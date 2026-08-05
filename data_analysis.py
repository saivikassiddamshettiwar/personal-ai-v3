import pandas as pd
import matplotlib.pyplot as plt


def load_data(uploaded_file):

    file_name = uploaded_file.name.lower()

    if file_name.endswith(".csv"):

        return pd.read_csv(uploaded_file)

    elif file_name.endswith(".xlsx"):

        return pd.read_excel(
            uploaded_file,
            engine="openpyxl"
        )

    elif file_name.endswith(".xls"):

        return pd.read_excel(
            uploaded_file,
            engine="xlrd"
        )

    else:

        raise ValueError(
            "Unsupported file format"
        )


def get_data_summary(df):

    return {

        "rows": len(df),

        "columns": len(df.columns),

        "column_names": list(
            df.columns
        )

    }


def create_chart(
    df,
    selected_column
):

    if selected_column not in df.columns:

        return None

    fig, ax = plt.subplots()

    df[selected_column].plot(
        kind="bar",
        ax=ax
    )

    ax.set_title(
        selected_column
    )

    ax.set_xlabel(
        "Row"
    )

    ax.set_ylabel(
        selected_column
    )

    plt.tight_layout()

    return fig