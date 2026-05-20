import os
from pathlib import Path
import polars as pl
from src.infrastructure.templates.ProcessorTemplate import ProcessorTemplate

class CSVProcessor(ProcessorTemplate):
    def __init__(self, root_folder : str, separator : str = '\t') -> None:
        self.root_folder = root_folder
        self.separator = separator
        self._files : list[Path] = []
    def get_files(self) -> list[Path]:
        if not self._files:
            self._files = [f for f in Path(self.root_folder).iterdir() if f.is_file()]
        return self._files
    def load_files(self) -> list[pl.LazyFrame]:
        return [
            pl.scan_csv(str(f), separator=self.separator, infer_schema_length=0)
            for f in self.get_files()
        ]
    def save_data(self, lf : pl.LazyFrame, output_folder : str, filename : str = "output") -> None:
        output = Path(output_folder)
        output.mkdir(parents=True, exist_ok=True)

        file_path = os.path.join(output, f'{filename}.csv')
        lf.collect().write_csv(file_path, separator=',')

    def add_prefix(self, lfs: list[pl.LazyFrame]) -> list[pl.LazyFrame]:
        return [
            lf.select(
                pl.col("DATE"),
                pl.all().exclude("DATE").name.prefix(f"{f.stem}_")
            )
            for lf, f in zip(lfs, self.get_files())
        ]
    @staticmethod
    def concat_time_cols(lfs: list[pl.LazyFrame]) -> list[pl.LazyFrame]:
        return [
            lf.with_columns(
                pl.concat_str([pl.col("DATE"), pl.col("TIME")], separator=" ").alias("DATE")
            ).drop("TIME")
            for lf in lfs
        ]
    @staticmethod
    def apply_clean_borders(lf: pl.LazyFrame) -> pl.LazyFrame:
        lf_i    = lf.with_row_index("row_nr")
        started = pl.all_horizontal(pl.all().exclude("DATE", "row_nr").is_not_null())
        first   = lf_i.filter(started).select(pl.col("row_nr").min()).collect().item()
        last    = lf_i.filter(started).select(pl.col("row_nr").max()).collect().item()
        return lf_i.filter(
            (pl.col("row_nr") >= first) & (pl.col("row_nr") <= last)
        ).drop("row_nr")
    
    @staticmethod
    def clean_cols(lfs: list[pl.LazyFrame]) -> list[pl.LazyFrame]:
        return [
            lf.select(pl.all().name.replace(r"[<>]", ""))
            for lf in lfs
        ]

    @staticmethod
    def apply_linear_interpolate(lf: pl.LazyFrame) -> pl.LazyFrame:
        return lf.with_columns(
            pl.all().exclude("DATE").cast(pl.Float64).interpolate(method='linear')
        )
    
    def process_data(self, output_folder : str = 'output') -> None:
        lfs = self.load_files()
        lfs = self.clean_cols(lfs)
        lfs = self.concat_time_cols(lfs)
        lfs = self.remove_useless_cols(lfs, ['SPREAD','VOL'])
        lfs = self.add_prefix(lfs)
        lf  = self.concat_lfs(lfs)
        lf  = self.apply_clean_borders(lf)
        lf  = self.apply_linear_interpolate(lf)
        self.save_data(lf, output_folder)