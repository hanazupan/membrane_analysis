import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


sns.set_context("paper")
sns.set_style("whitegrid")
sns.set_palette("hls", 5)


def plot_density_profile(df: pd.DataFrame):
    print(df)
    df.plot(x="Position [nm]")
    plt.gca().set_ylabel("Density [kg/m^3]")
    return plt.gcf(), plt.gca()


# path = "/home/hanaz63/nobackup/membrane_things/clean_try_F13/"
# df = pd.read_csv(f"{path}distance", delimiter="\t")
#
# df.columns = ["Frame", "ETE Distance [A]"]
# df["ETE Distance [nm]"] = df["ETE Distance [A]"]/10
#
# df.plot(x="Frame", y="ETE Distance [nm]", legend=False)
# plt.gca().set_ylabel("ETE Distance [nm]")
# plt.savefig(f"{path}end_to_end_distance_F13.png", dpi=600)