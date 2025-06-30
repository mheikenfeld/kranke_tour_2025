# %%
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt


excel_path = Path(
    r"C:\Users\BenediktZarl\OneDrive - Deutsche Bahn\98_Arbeitsumgebung\Kranke Tour\2025\Lose_2025.xlsx"
)

# Load Excel file (update filename as needed)
df = pd.read_excel(excel_path, sheet_name="Losmaschine")
output_dir = excel_path.parent


# %%

unique_lostopf = df["Lostopf"].dropna().unique()
colors = plt.cm.get_cmap(
    "tab20", len(unique_lostopf)
)  # Use "tab20" for up to 20 distinct colors
lostopf_color_map = {
    str(val): f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"
    for val, (r, g, b, _) in zip(unique_lostopf, colors(range(len(unique_lostopf))))
}

js_color_map = (
    "const lostopfColors = {\n"
    + "\n".join([f'  "{k}": "{v}",' for k, v in lostopf_color_map.items()])
    + '\n  "default": "gray"\n};\n'
)

# Assume the columns are named or ordered like this:
lat_col = "Breitengrad Bahnhof"
lon_col = "Längengrad Bahnhof"
meta_cols = [
    "ID",
    "Bahnhof",
    "Zeit- bedarf",
    "Distanz in km",
    "Punkte Bahnhof",
    "Punkte Aufgabe",
    "Lostopf",
]  # Add your meta columns here
js_array = "const coordinates = [\n"
for _, row in df.iterrows():
    js_array += (
        "  { "
        f"latitude: {row[lat_col]}, longitude: {row[lon_col]}, "
        + ", ".join(
            [
                f'{col.lower().replace(" ", "_").replace("-", "_").replace("(", "").replace(")", "")}: "{row[col]}"'
                for col in meta_cols
            ]
        )
        + " },\n"
    )
js_array += "];\n"
# Save as coordinates.js
js_path = output_dir / "coordinates.js"
with open(js_path, "w", encoding="utf-8") as f:
    f.write(js_color_map)
    f.write(js_array)

bhf_paar = df[df["Lostopf"] == "Bhf-Paare"]
bhf_paar_groups = bhf_paar.groupby("ID")

js_lines = "const bhfPaarLines = [\n"
for id_val, group in bhf_paar_groups:
    if len(group) > 1:
        coords = [f"[{row[lat_col]}, {row[lon_col]}]" for _, row in group.iterrows()]
        js_lines += f'  [{", ".join(coords)}],\n'
js_lines += "];\n"

with open(js_path, "a", encoding="utf-8") as f:
    f.write(js_lines)

print("✅ coordinates.js generated successfully.")

# %%
