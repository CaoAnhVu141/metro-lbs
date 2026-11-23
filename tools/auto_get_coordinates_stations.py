import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

df = pd.read_csv("data/stations.csv", encoding="utf-8")
df["lat"] = pd.to_numeric(df["lat"], errors="coerce")
df["lon"] = pd.to_numeric(df["lon"], errors="coerce")

# init Nominatim
geolocator = Nominatim(user_agent="metro_lbs_hcm_project", timeout=10)
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1.1)

# Expanded HCM city (including Binh Duong & Vung Tau)
HCM_VIEWBOX = [(10.3, 106.3), (11.6, 107.6)]


def get_coords(place_name):
    # queries = [
    #     f"ga {place_name}, Thành phố Hồ Chí Minh, Việt Nam",
    #     f"ga {place_name}, Việt Nam",
    # ]
    queries = [
        f"{place_name}, Thành phố Hồ Chí Minh, Việt Nam",
        f"{place_name}, Việt Nam",
    ]
    for q in queries:
        loc = geocode(q, viewbox=HCM_VIEWBOX, country_codes="vn")
        if loc and (10.3 <= loc.latitude <= 11.6) and (106.3 <= loc.longitude <= 107.6):
            return round(loc.latitude, 6), round(loc.longitude, 6)
    return None, None


# searching for line don't have lat/lon
for idx, row in df.iterrows():
    if pd.isna(row["lat"]) or pd.isna(row["lon"]):
        lat, lon = get_coords(row["ten"])
        df.at[idx, "lat"] = lat
        df.at[idx, "lon"] = lon
        print(f"[{idx+1}/{len(df)}] {row['ten']} -> ({lat}, {lon})")

# overwrite file
df = df[["ten", "tuyen", "trang_thai", "lat", "lon"]]
df.to_csv("data/stations.csv", index=False, encoding="utf-8")

# report that line can't find
missing = df[df["lat"].isna() | df["lon"].isna()]
print(f"\nHoan tat! Con {len(missing)} ga chua co toa do:")
if not missing.empty:
    print(missing[["ten", "tuyen", "trang_thai"]])
