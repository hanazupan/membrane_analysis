import matplotlib.pyplot as plt
import numpy as np
import MDAnalysis as mda
import seaborn as sns
import pandas as pd

path = "/home/hanaz63/nobackup/membrane_things/POPC_with_F13/version2/"
#path = "/home/hanaz63/nobackup/membrane_things/POPC_with_C12/version1/"
#path = "/home/hanaz63/nobackup/membrane_things/POPC_with_C12/version2/"
#path = "/home/hanaz63/nobackup/membrane_things/another_POCP_with_R10K/variant1/"
#path = "/home/hanaz63/nobackup/membrane_things/another_POCP_with_R10K/variant2/"

#TODO: combine data from different versions

sns.set_context("paper")
sns.set_style("whitegrid")
sns.set_palette("hls", 5)

def read_xvg(filepath):
    # Read the file, skipping metadata lines
    with open(filepath, 'r') as f:
        lines = [line for line in f if not line.startswith(('@', '#'))]

    # Use pandas to read the remaining lines
    from io import StringIO
    data = pd.read_csv(StringIO(''.join(lines)), delim_whitespace=True, header=None)
    return data


#density_PC.xvg density_pept.xvg density_PA.xvg density_OL.xvg
density_PC = read_xvg(f"{path}density_PC.xvg")
density_PC.columns = ["Position [nm]", "PC"]
density_PA = read_xvg(f"{path}density_PA.xvg")
density_PA.columns = ["Position [nm]", "PA"]
density_OL = read_xvg(f"{path}density_OL.xvg")
density_OL.columns = ["Position [nm]", "OL"]
density_pept = read_xvg(f"{path}density_ARG.xvg")
density_pept.columns = ["Position [nm]", "polypeptide"]
density_tag = read_xvg(f"{path}density_LFS.xvg")
density_tag.columns = ["Position [nm]", "tag"]


df = density_PC.merge(density_PA, on=density_PC.columns[0]) \
               .merge(density_OL, on=density_PC.columns[0]) \
               .merge(density_tag, on=density_tag.columns[0]) \
               .merge(density_pept, on=density_PC.columns[0])


df.plot(x="Position [nm]")
plt.gca().set_ylabel("Density [kg/m^3]")
#plt.gca().set_xlim(0.5, 5)
#plt.gca().set_ylim(0, 70)
#plt.show()
plt.savefig(f"{path}density_z_axis.png", dpi=600)


df_sorted = df.sort_values(by="PC", ascending=False)
print(df_sorted.head(10))


# path = "/home/hanaz63/nobackup/membrane_things/clean_try_F13/"
# df = pd.read_csv(f"{path}distance", delimiter="\t")
#
# df.columns = ["Frame", "ETE Distance [A]"]
# df["ETE Distance [nm]"] = df["ETE Distance [A]"]/10
#
# df.plot(x="Frame", y="ETE Distance [nm]", legend=False)
# plt.gca().set_ylabel("ETE Distance [nm]")
# plt.savefig(f"{path}end_to_end_distance_F13.png", dpi=600)