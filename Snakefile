
#my_path = "/home/hanaz63/nobackup/membrane_things/POPC_with_F13/version2/"
my_path = "/home/hanaz63/nobackup/membrane_things/POPC_with_C12/version2/"

DENSITY_CATEGORIES = file_name=["PC", "PA", "OL", "pept"]

rule make_all:
    input:
        f"{my_path}density_z_axis.png",
        f"{my_path}along_traj.png"


rule make_membrane_density_plot:
    input:
        all_xvg = expand(f"{my_path}density_{{file_name}}.xvg", file_name=DENSITY_CATEGORIES)
    output:
        density_plot = f"{my_path}density_z_axis.png"
    run:
        from readers_writers import merge_multiple_xvg
        from membrane_density_profile import plot_density_profile

        merged_df = merge_multiple_xvg(input.all_xvg, "Position [nm]", DENSITY_CATEGORIES)

        fig, ax = plot_density_profile(merged_df)
        fig.savefig(output.density_plot, dpi=600)

rule get_membrane_width:
    input:
        density = f"{my_path}density_PC.xvg"
    run:
        from readers_writers import read_xvg

        df = read_xvg(input.density)
        df.columns = ["Position [nm]", "PC"]
        df_sorted = df.sort_values(by="PC",ascending=False)

        position_max1 = df_sorted.iloc[0]["Position [nm]"]
        position_max2 = df_sorted.iloc[1]["Position [nm]"]
        assert position_max1*position_max2 < 0, "Whoops one minimum should be + and one -"

        membrane_width = abs(position_max1)+abs(position_max2)
        print(f"Average membrane width is {membrane_width} nm.")


TRAJECTORY_FILES = ["arg", "tag", "memb_u", "memb_l"]
rule position_of_polypeptide_in_time:
    input:
        xvg_files = [f"{my_path}{what}.xvg" for what in TRAJECTORY_FILES]
    output:
        plot = f"{my_path}along_traj.png"
    run:
        from readers_writers import read_xvg
        import matplotlib.pyplot as plt
        import seaborn as sns

        sns.set_context("paper")
        sns.set_style("whitegrid")
        sns.set_palette("hls",5)
        fig, ax = plt.subplots(1,1)

        colors = ["red", "blue", "black", "black"]

        for input_file, label, color in zip(input.xvg_files, TRAJECTORY_FILES, colors):
            df = read_xvg(input_file)
            df.columns = ["Frame", "Position x [nm]", "Position y [nm]", "Position z [nm]"]
            df.plot.scatter(x="Frame", y="Position z [nm]",  s=1, c=color, ax=ax, label=label)

        plt.savefig(output.plot, dpi=600)

