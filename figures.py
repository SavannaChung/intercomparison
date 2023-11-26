import matplotlib.pyplot as plt

import config as cg
import functions as fn



def plot_drift(ss_dict, ss_tpc, ssr_dict, ssr_tpc):
    ''' assess any drift between two datasets'''


    ss_ave, ss_std = fn.calc_ave_std(ss_dict, ss_tpc)
    ssr_ave, ssr_std = fn.calc_ave_std(ssr_dict, ssr_tpc)


    # create en in a list
    ens = [float(e) for e in cg.pro_en]

    ssmssr = {}
    pssmssr = {}
    for en in cg.pro_en:
        d = ss_ave[en] - ssr_ave[en]

        # append ss_dict
        p = 100*d/ss_ave[en]
        ssmssr.update({en:d})
        pssmssr.update({en:p})

    fig, axes = plt.subplots(nrows =2, ncols =1, sharex = True, figsize = (5, 6))
    # axes[0].plot(ens, list(ss_ave.values()), 'ko', fillstyle = 'none')
    # axes[0].plot(ens, list(ssr_ave.values()), 'r+')
    # axes[0].set_ylabel('measured nC')
    # axes[0].set_title('TPC corrected')
    # axes[0].set_xlim(60, 250)

    axes[0].plot(ens, list(ssmssr.values()), 'k^', fillstyle = 'none')
    axes[0].axhline(y=0, color='gray')
    axes[0].set_ylabel('diff(nC)')
    axes[0].set_title('TPC corrected, ss-ssr', fontsize = 8)
    axes[0].set_xlim(60, 250)

    axes[1].plot(ens, list(pssmssr.values()), 'ks', fillstyle='none')
    axes[1].axhline(y=0, color='gray')
    axes[1].set_ylabel('percentage diff. (%)')
    axes[1].set_title('TPC corrected nC, 100*(ss-ssr)/ss', fontsize = 8)

    fig.supxlabel('proton energy (MeV)')
    plt.tight_layout()
    plt.savefig('ss_drift.png')
    # plt.show()
