import pandas as pd
from docling_core.transforms.chunker import HierarchicalChunker
from docling_core.types.doc.document import TableItem

def detect_and_merge_header(df, threshold=0.6):
    """
    Detect and merge header rows in a DataFrame.

    Args:
        df: DataFrame need to be processed
        threshold: minimum ratio of matching columns to consider as header

    Returns:
        DataFrame processed and a boolean value indicating whether header rows are detected
    """
    # detect header rows
    potential_headers = min(5, len(df))
    header_rows = []

    # compare each pair of rows
    for i in range(potential_headers):
        for j in range(i + 1, potential_headers):
            # Đếm số cột trùng nhau
            matching_cols = sum(df.iloc[i] == df.iloc[j])
            if matching_cols / len(df.columns) >= threshold:
                if i not in header_rows:
                    header_rows.append(i)
                if j not in header_rows:
                    header_rows.append(j)

    if not header_rows:
        return df, False

    # merge headers
    headers = df.iloc[header_rows].astype(str)
    merged_header = headers.apply(lambda x: ' '.join(filter(None, x.unique())), axis=0)

    # create new DataFrame without header rows and set new header
    new_df = df.drop(header_rows).reset_index(drop=True)
    new_df.columns = merged_header

    return new_df, True


@classmethod
def _format_table_rows(cls, table_df: pd.DataFrame) -> str:
    """
    Converts DataFrame to format:
    row1: headercol1=value, headercol2=value,...
    row2: headercol1=value, headercol2=value,...
    Args:
        table_df (pd.DataFrame): DataFrame to format
    Returns:
        str: formatted text
    """
    # Get headers
    headers = table_df.columns.tolist()

    # Process each row
    rows = []
    for idx, row in table_df.iterrows():
        # Format each cell as "header=value"
        cells = [f"{headers[i]}={str(val).strip()}" for i, val in enumerate(row)]
        # Combine cells with commas
        row_text = f"row{idx + 1}: " + ", ".join(cells)
        rows.append(row_text)

    # Join all rows with newlines
    return "\n".join(rows)


original_function = TableItem.export_to_dataframe


def export_to_dataframe_new(self) -> pd.DataFrame:
    """
    Export table item to DataFrame. If header rows are detected, merge them and return the new DataFrame.
    Args:
        self: TableItem object

    Returns:
        pd.DataFrame: Exported DataFrame
    """
    # print("⚡ export_to_dataframe_new is called!")
    df = original_function(self)

    df_new, check = detect_and_merge_header(df)
    if check:
        return df_new
    else:
        HierarchicalChunker._triplet_serialize = _format_table_rows
        return df


TableItem.export_to_dataframe = export_to_dataframe_new
