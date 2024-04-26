import os
import scipy as sp
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import MaxNLocator
from Matrix import *
import argparse

# Adjust Plots Style
plt.style.use('seaborn-v0_8')
plt.rc('font', family='serif')
plt.rc('xtick', labelsize='x-small')
plt.rc('ytick', labelsize='x-small')
fmt = 'png'

fig_save_opts = {'format': fmt , 'dpi':1000, 'bbox_inches':'tight'}

disp_name = {
             'deg': 'Degree',
             'in-deg': 'In-Degree',
             'out-deg': 'Out-Degree',
             'clustering': 'Clustering Coefficient',
             'diameter': 'Diameter',
             'avg-shortest-path-length': 'Average Shortest Path Length',
             'betweenness-centrality': 'Betweenness Centrality',
             'eigenvector-centrality': 'Eigenvector Centrality',
             'laplacian-centrality': 'Laplacian Centrality',
             'closeness-centrality' : 'Closeness Centrality',
             'hop-count': 'Hop Count',
             'scree': 'Scree Plot'
             }

def float_range(value):
    min_value = 0.0
    max_value = 1.0

    try:
        fvalue = float(value)
        if min_value <= fvalue <= max_value:
            return fvalue
        raise argparse.ArgumentTypeError(f'{value} must be between [{min_value}, {max_value}]')
    except ValueError:
        raise argparse.ArgumentTypeError(f'{value} is not a valid float')

def plotHistLine(vector, ax, label):
    hist, bins = np.histogram(vector)
    norm_hist = hist.astype(np.float32) / hist.sum()
    bin_centers = 0.5 * (bins[1:] + bins[:-1])
    sns.lineplot(x=bin_centers, y=norm_hist, ax=ax, marker='D', label=label)

def plotGraph(graph, outfile):
    fig , ax = plt.subplots()
    nx.draw(graph, with_labels=True,node_color='lightblue', edge_color='red', pos=nx.kamada_kawai_layout(graph), ax=ax)
    fig.savefig(f'{outfile}.{fmt}', **fig_save_opts)

    plt.close(fig)

def plotSpy(adjMat, outfile):
    fig1, ax1 = plt.subplots()
    ax1.spy(adjMat)
    fig1.savefig(f'{outfile}.{fmt}', **fig_save_opts)
    plt.close(fig1)

def plotKde(vector, ax, idx, label):    # check if passing index, label correctly
    addStyle = {}
    if idx == 0:
        addStyle = {'linestyle':'--', 'color':'black'}
    sns.kdeplot(vector, ax=ax, label=label, **addStyle)

def plotHist(vector, outfile, percent=False):
    fig, ax = plt.subplots()
    stat = 'percent' if percent else 'count'
    sns.histplot(vector, ax=ax, stat=stat)
    fig.savefig(f'{outfile}.{fmt}', **fig_save_opts)
    plt.close(fig)


def plotKdeOnHist(vector, outfile, vec_label='Degree'):
    fig, ax = plt.subplots()
    sns.histplot(vector, kde=True, stat='percent', ax=ax)
    ax.set_xlabel(vec_label)
    ax.set_ylabel('Percent')
    fig.savefig(f'{outfile}.{fmt}', **fig_save_opts)
    plt.close(fig)


def plotLine(x_values, y_values, ax, label):
    addStyle = {}
    if label == 'no_noise':
        addStyle = {'linestyle':'--', 'color':'black'}
    sns.lineplot(x=x_values,y=y_values,ax=ax,label=label,markers='o', **addStyle)

def plotScalar(x_values, y_values,x_label,y_label,outfile):
    if not y_values:
        return
    fig, ax = plt.subplots()
    plotLine(x_values, y_values, ax, None)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    fig.savefig(f'{outfile}.{fmt}', **fig_save_opts)
    plt.close(fig)

# Accumlates multiple plots on the same figure
def finalize_acc_plot(figs_dict,kPower,plot_type,outdir): 
    for k in figs_dict.keys():
        if figs_dict[k] != None and figs_dict[k][0] != None and figs_dict[k][1] != None:
            if k == 'scree':
                figs_dict[k][1].set_xlabel('Rank')
                figs_dict[k][1].set_ylabel('Singular Value')
                plot_type = ''
            elif k == 'hop-count':
                figs_dict[k][1].set_xlabel('Number of Hops')
                figs_dict[k][1].set_ylabel('Number of Reachable Pairs')
                plot_type = ''
            else:
                figs_dict[k][1].set_xlabel(disp_name[k])
            figs_dict[k][1].xaxis.set_major_locator(MaxNLocator(integer=True))
            figs_dict[k][1].legend()
            figs_dict[k][0].savefig(f'{outdir}/k{kPower}_{k}_{plot_type}.{fmt}', **fig_save_opts)
            plt.close(figs_dict[k][0])


def main():
    # TODO: add as parameters
    init_values = [0.999, 0.437, 0.437, 0.484]
    kron_times = 5
    supported_plots = ['kde','hist-line','hist','kde_hist','graph','spy']

    # different options for plotting
    # kde, hist_line, hist, kde_hist, graph, spy
    # only kde and hist_line plot multiple plots on the same figure

    parser = argparse.ArgumentParser()

    parser.add_argument('--p', metavar='P', nargs=4, type=float_range, required=True, help='Initiator probability matrix')
    parser.add_argument('--plots', metavar='F', nargs='+', help='type of plot (kde, hist-line, hist, kde_hist, graph, spy)', choices=supported_plots, default=[])
    parser.add_argument('--props', metavar='Pr', nargs='+', choices=disp_name.keys(), help='Graph properties to calculate and plot', default=[])
    parser.add_argument('--k', type=int, required=True, help='Kronecker Power')
    parser.add_argument('--outdir', type=str, default='./plotRepo', help='Output directory for the plots')

    args = parser.parse_args()

    print(f'Initiator Matrix: {args.p}')
    print(f'Kronecker Power: {args.k}')
    print(f'Requested Plots: {args.plots}')
    print(f'Output Directory: {args.outdir}')

    if (not os.path.exists(args.outdir)):
        os.makedirs(args.outdir)
        print(f'Directory created')
    else:
        print(f'Directory already exists')

    init_values = args.p
    kron_times = args.k
    plots = {}
    props = {}
    for plot in args.plots:
        plots[plot] = True
    for prop in args.props:
        props[prop] = True

    kde_fig_axis = {}
    hist_line_fig_axis = {}
    line_fig_axis = {}
    diameters = []
    avg_shortest_path_lengths = []
    xs = []

    for prop in props.keys():
        if prop in ['hop-count','scree']:
            line_fig_axis[prop] = [None, None]
        elif prop in ['avg-shortest-path-length', 'diameter']:
            print('scalars')
        else:
            if plots.get('kde', False):
                kde_fig_axis[prop] = [None, None]
            if plots.get('hist-line', False):
                hist_line_fig_axis[prop] = [None, None]



    for graph_prop in kde_fig_axis.keys():
        kde_fig_axis[graph_prop] = list(plt.subplots())

    for graph_prop in hist_line_fig_axis.keys():
        hist_line_fig_axis[graph_prop] = list(plt.subplots())

    for graph_prop in line_fig_axis.keys():
        line_fig_axis[graph_prop] = list(plt.subplots())


    new_init = init_values.copy()

    init_Mat = Initiator(new_init)

    kron_mat = kront(init_Mat,kron_times).tocoo()

    kron_mat = mask(kron_mat)

    rows, cols = kron_mat.shape


    alpha = 0.005
    for j in range(6):
        vectors = {}
        scalars = {}
        in_deg = out_deg =  None
        #new_init[i] = new_init[i] - 0.1 if i == 0 else new_init[i] + 0.1

        #xs.append(new_init[i])

        if j == 0:
            names_suffix = f'no_noise'
            label = names_suffix
            names_suffix = f'k{args.k}_{names_suffix}'
            adj_mat = kron_mat
        else:
            names_suffix = f'alpha_{alpha:.3f}'
            label = names_suffix.replace('_','=')
            names_suffix = f'k{args.k}_{names_suffix}'
            noise = sp.sparse.random(rows, cols, density=alpha)
            adj_mat = kron_mat + noise

        graph = nx.from_scipy_sparse_array(adj_mat, create_using=nx.DiGraph())
        print(graph)

        if plots.get('graph',False):
            plotGraph(graph,f'{args.outdir}/graph_{names_suffix}')

        if plots.get('spy', False):
            plotSpy(adj_mat,f'{args.outdir}/spy_{names_suffix}')

        print(f'number of nodes: {graph.number_of_nodes()}')
        # Total Degree for nodes

        if props.get('deg', False):
            vectors['deg'] = [degree for _,degree in graph.degree()]

        # Clustering Co-efficient for nodes
        if props.get('clustering', False):
            vectors['clustering'] = list(nx.clustering(graph).values())

        if props.get('in-deg', False):
            vectors['in-deg'] = [in_degree for _,in_degree in graph.in_degree()]

        if props.get('out-deg', False):
            vectors['out-deg'] = [out_degree for _,out_degree in graph.out_degree()]

        if props.get('diameter', False):
            try:
                diameters.append(nx.diameter(graph.to_undirected()))
            except:
                diameters.append(10000000)

        # Betweenness Centrality for nodes
        if props.get('betweenness-centrality', False):
            vectors['betweenness-centrality'] = list(nx.betweenness_centrality(graph).values())

        # Eigenvalues : RAISES a NetworkXNotImplemented for directed type
        #L = nx.normalized_laplacian_matrix(graph)
        #e = np.linalg.eigvals(L.toarray())
        #print(f'eigenvalues = {e}')

        # Eigenvector centrality
        if props.get('eigenvector-centrality', False):
            vectors['eigenvector-centrality'] = list(nx.eigenvector_centrality(graph).values())

        if props.get('laplacian-centrality', False):
            vectors['laplacian-centrality'] = list(nx.laplacian_centrality(graph).values())

        if props.get('hop-count', False):
            reachable_pairs = []
            vectors['hop-count'] = {}
            for hops in range(nx.diameter(graph) +1):
                reachable_pairs.append(len(list(nx.all_pairs_shortest_path_length(graph, cutoff=hops))))
            print(f'reachable-pairs = {reachable_pairs}')
            vectors['hop-count']['y'] = reachable_pairs
            vectors['hop-count']['x'] = range(len(reachable_pairs))
            xlbl = 'Number of Hops'
            ylbl = 'Number of Reachable Pairs'
            plotLine(vectors['hop-count']['x'], vectors['hop-count']['y'], line_fig_axis['hop-count'][1],label=label)

        if props.get('scree', False):
            vectors['scree'] = {}
            A = nx.to_numpy_array(graph)
            U, vectors['scree']['y'], V = np.linalg.svd(A)
            # rank
            vectors['scree']['x'] = range(1, len(vectors['scree']['y'])+1)
            plotLine(vectors['scree']['x'], vectors['scree']['y'], line_fig_axis['scree'][1], label=label)

        if props.get('avg-shortest-path-length', False):
            try:
                avg_shortest_path_lengths.append(nx.average_shortest_path_length(graph.to_undirected()))
            except:
                avg_shortest_path_lengths.append(10000)

        if props.get('closeness-centrality', False):
            vectors['closeness-centrality'] = list(nx.closeness_centrality(graph).values())

        if plots.get('hist-line', False):
            for graph_prop in hist_line_fig_axis.keys():
                plotHistLine(vectors[graph_prop], hist_line_fig_axis[graph_prop][1], label=label)

        if plots.get('kde', False):
            for graph_prop in kde_fig_axis.keys():
                plotKde(vectors[graph_prop], kde_fig_axis[graph_prop][1],j, label=label)

        if plots.get('kde_hist', False):
            for vec in vectors.keys():
                plotKdeOnHist(vectors[vec], f'{args.outdir}/hist_kde_{vec}_{names_suffix}')


        if plots.get('hist', False):
            for vec in vectors.keys():
                plotHist(vectors[vec], f'{args.outdir}/hist_{vec}_{names_suffix}')

        alpha *= 2
    finalize_acc_plot(kde_fig_axis, args.k,'kde', args.outdir)
    finalize_acc_plot(hist_line_fig_axis, args.k, 'hist_line', args.outdir)
    finalize_acc_plot(line_fig_axis, args.k, 'line', args.outdir)

    if props.get('diameter', False):
        plotScalar(xs,diameters,f'alpha','Diameter',f'{args.outdir}/k{args.k}_alpha{alpha}_diameter')

    if props.get('avg-shortest-path-length', False):
        plotScalar(xs,avg_shortest_path_lengths,f'alpha', 'Avg. Shortest Path Length',f'{args.outdir}/k{args.k}_alpha{alpha}_avg-shortest-path-length')


main()

