import os
import glob
import math
#import snap
import scipy as sp
import numpy as np
import networkx as nx

#import cudf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as ticker
from matplotlib.ticker import MaxNLocator
from Matrix import *


force_use_cpu = False
try:
    import cugraph
except ImportError:
    print(f'Cannot find cuGraph, forcing networkx')
    force_use_cpu = True


#device_index = 0
#device = cp.cuda.Device(device_index)
#device.use()


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

# A function to convert a snap graph into a networkx directed graph
'''
def snap_to_nx(snap_g):
    nx_g = nx.DiGraph()
    for node in snap_g.Nodes():
        nx_g.add_node(node.GetId())
    for edge in snap_g.Edges():
        src = edge.GetSrcNId()
        dst = edge.GetDstNId()
        nx_g.add_edge(src, dst)

    return nx_g
'''

def edgelist_to_scipy(edgelist):
    data = pd.read_csv(edgelist, sep='\t', comment='#', names=['from', 'to'])

    rows = data['from']
    cols = data['to']
    nodes = max(max(rows), max(cols))
    ones = np.ones(len(rows), np.float32)
    return sp.sparse.coo_matrix((ones, (rows, cols)), (nodes, nodes))

# A function to calculate all graph properties
def calcProps(nx_g,props,device='cpu'):
    # Calculate the original graph stuff
    vectors_orig = {}

    if device == 'cpu' or force_use_cpu:

        if props.get('deg', False):
            vectors_orig['deg'] = [degree for _,degree in nx_g.degree()]
            #vectors_orig['deg'] = list(cnx.degree_centrality(nx_g).values())

        # Clustering Co-efficient for nodes
        #if props.get('clustering', False):
        #    vectors_orig['clustering'] = list(nx.clustering(nx_g).values())

        if props.get('in-deg', False):
            vectors_orig['in-deg'] = [in_degree for _,in_degree in nx_g.in_degree()]
            #vectors_orig['in-deg'] = cu_g.in_degree()['degree'].to_arrow().to_pylist()

        if props.get('out-deg', False):
            vectors_orig['out-deg'] = [out_degree for _,out_degree in nx_g.out_degree()]
            #vectors_orig['out-deg'] = list(cnx.out_degree_centrality(nx_g).values())

        if props.get('betweenness-centrality', False):
            vectors_orig['betweenness-centrality'] = list(nx.betweenness_centrality(nx_g).values())

        #if props.get('closeness-centrality', False):
        #    vectors_orig['closeness-centrality'] = list(nx.closeness_centrality(nx_g).values())

        # Eigenvector centrality
        if props.get('eigenvector-centrality', False):
            vectors_orig['eigenvector-centrality'] = list(nx.eigenvector_centrality(nx_g).values())


        #if props.get('laplacian-centrality', False):
        #    vectors_orig['laplacian-centrality'] = list(nx.laplacian_centrality(nx_g).values())

        #if props.get('scree', False):
        #    vectors_orig['scree'] = {}
        #    A = nx.to_numpy_array(nx_g)
        #    U, vectors_orig['scree']['y'], V = np.linalg.svd(A)
            # rank
        #    vectors_orig['scree']['x'] = range(1, len(vectors_orig['scree']['y'])+1)
    else:
        if props.get('deg', False):
            vectors_orig['deg'] = nx_g.degree()['degree']
            vectors_orig['deg'] = vectors_orig['deg'].to_numpy()
        # Clustering Co-efficient for nodes
        # not directly supported in cugraph
        #if props.get('clustering', False):
        #    vectors_orig['clustering'] = list(nx.clustering(nx_g).values())

        if props.get('in-deg', False):
            vectors_orig['in-deg'] = nx_g.in_degree()['degree']
            vectors_orig['in-deg'] = vectors_orig['in-deg'].to_numpy()


        if props.get('out-deg', False):
            vectors_orig['out-deg'] = nx_g.out_degree()['degree']
            vectors_orig['out-deg'] = vectors_orig['out-deg'].to_numpy()



        if props.get('betweenness-centrality', False):
            vectors_orig['betweenness-centrality'] = cugraph.centrality.betweenness_centrality(nx_g)['betweenness_centrality']
            vectors_orig['betweenness-centrality'] = vectors_orig['betweenness-centrality'].to_numpy()


        # Not supported in cuGraph
        #if props.get('closeness-centrality', False):
        #    vectors_orig['closeness-centrality'] = list(nx.closeness_centrality(nx_g).values())

        # Eigenvector centrality
        if props.get('eigenvector-centrality', False):
            vectors_orig['eigenvector-centrality'] = cugraph.centrality.eigenvector_centrality(nx_g)['eigenvector_centrality']
            vectors_orig['eigenvector-centrality'] = vectors_orig['eigenvector-centrality'].to_numpy()


        if props.get('katz-centrality', False):
            vectors_orig['katz-centrality'] = cugraph.centrality.katz_centrality(nx_g)['katz_centrality']
            vectors_orig['katz-centrality'] = vectors_orig['katz-centrality'].to_numpy()

        if props.get('edge-betweenness-centrality', False):
            vectors_orig['edge-betweenness-centrality'] = cugraph.centrality.edge_betweenness_centrality(nx_g)['edge_betweenness_centrality']
            vectors_orig['edge-betweenness-centrality'] = vectors_orig['edge-betweenness-centrality'].to_numpy()
        # Not supported directly in cuGraph
        #if props.get('laplacian-centrality', False):
        #    vectors_orig['laplacian-centrality'] = list(nx.laplacian_centrality(nx_g).values())

        # Not directly supported in cuGraph
        if props.get('scree', False):
            vectors_orig['scree'] = {}
            A = cp.array(cugraph.to_numpy_array(nx_g))
            U, vectors_orig['scree']['y'], V = cp.linalg.svd(A)
            # rank
            vectors_orig['scree']['x'] = range(1, len(vectors_orig['scree']['y'])+1)



    return vectors_orig

def dumpData(vectors, names_suffix, outdir):

    gdf = pd.DataFrame()

    if (not os.path.exists(f'{outdir}/data')):
        os.makedirs(f'{outdir}/data')
        print(f'Data Directory created')
    else:
        print(f'Data Directory already exists')

    for prop in vectors:
        gdf[prop] = vectors[prop]


    out_file_path = f"{outdir}/data/{names_suffix.replace('*','')}_vectors.csv"

    gdf.to_csv(out_file_path, index=False)
    print(f"Graph calculated vectors saved to {out_file_path}")

# Loads the initiator matrix values, the Kronecker Power, and the number
# of nodes of the original graph from the restored files
def loadInfo(indir):
    init_vals = []
    with open(f'{indir}/data/info','r') as f:
        init_vals = [float(x) for x in f.readline().split(':')]
        kron_times = int(f.readline().split(':')[1])
        num_nodes = int(f.readline().split(':')[1])
    return init_vals, kron_times, num_nodes

# Loads the computed data for a given graph
# For the original graph, i should be -1 , j = -1, and init_vals = []
# For the synthetic graphs, i is the x index (x0, x1, ...) and j is
# the trial number (the index of the iteration at which the x[index] values is changed)
def loadData(indir, i, j, init_vals=[]):

    files_choices = glob.glob(f'{indir}/data/k*_x*_vectors.csv')
    a_file = os.path.basename(files_choices[0])

    k_value = int(a_file.split('_')[0][1:])


    if i == j == -1:
        file_name = f'k{k_value}_real_vectors.csv'
    else:
        if init_vals == []:
            with open(f'{indir}/data/info','r') as f:
                init_vals = [float(x) for x in f.readline().split(':')]
        x_idx = i
        if x_idx == 0:
            x_val = init_vals[i] - j * 0.1
        else:
            x_val = init_vals[i] + j * 0.1

        file_name = f'k{k_value}_x{x_idx}_{x_val:.3f}_vectors.csv'

    df = pd.read_csv(f'{indir}/data/{file_name}')
    vectors = {}

    for col in df.columns.tolist():
        vectors[col] = df[col]
    return vectors

def loadNoise(indir, alpha):

    file_name = f'noise_{alpha}_vectors.csv'
    df = pd.read_csv(f'{indir}/noise/data/{file_name}')
    vectors = {}
    for col in df.columns.tolist():
        vectors[col] = df[col]

    return vectors


def doPlot(plots, vectors, j, kde_fig_axis, line_fig_axis, hist_line_fig_axis, label, outdir, names_suffix):

    '''
    if plots.get('graph',False):
        plotGraph(graph,f'{outdir}/graph_{names_suffix}')
    '''

    if plots.get('spy', False):
        plotSpy(adj_mat,f'{outdir}/spy_{names_suffix}')

    if plots.get('hist-line', False):
        for graph_prop in hist_line_fig_axis.keys():
            plotHistLine(vectors[graph_prop], hist_line_fig_axis[graph_prop][1], label=label)

    if plots.get('kde', False):
        for graph_prop in kde_fig_axis.keys():
            plotKde(vectors[graph_prop], kde_fig_axis[graph_prop][1],j, label=label)

    if plots.get('kde_hist', False):
        for vec in vectors.keys():
            plotKdeOnHist(vectors[vec], f'{outdir}/hist_kde_{vec}_{names_suffix}')

    if plots.get('hist', False):
        for vec in vectors.keys():
            plotHist(vectors[vec], f'{outdir}/hist_{vec}_{names_suffix}')

    if vectors.get('scree', False):
        plotLine(vectors['scree']['x'], vectors['scree']['y'], line_fig_axis['scree'][1], label='real')


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

def plotKde(vector, ax,idx, label):
    addStyle = {}
    # Original Synthetic
    if idx == 0:
        addStyle = {'linestyle':'--', 'color':'black'}
    # Original Real
    if idx == -1:
        addStyle = {'linestyle': 'dotted', 'color':'grey'}
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
    sns.lineplot(x=x_values,y=y_values,ax=ax,label=label,markers='o')

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
def finalize_acc_plot(figs_dict,x_index,kPower,plot_type,outdir):
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

            #figs_dict[k][1].set_xscale('log', base=2)
            #figs_dict[k][1].set_yscale('log', base=2)

            figs_dict[k][1].xaxis.set_major_locator(MaxNLocator(integer=True))
            #figs_dict[k][1].xaxis.set_major_formatter(ticker.ScalarFormatter(useOffset=False, useMathText=True))
            figs_dict[k][1].xaxis.set_major_formatter(ticker.LogFormatter(labelOnlyBase=True))
            figs_dict[k][1].tick_params(axis='x', labelrotation=45)
            figs_dict[k][1].legend()
            if x_index == -1:
                # Noise Analysis figure
                figs_dict[k][0].savefig(f'{outdir}/k{kPower}_noise_{k}_{plot_type}.{fmt}', **fig_save_opts)
            else:
                figs_dict[k][0].savefig(f'{outdir}/k{kPower}_x{x_index}_{k}_{plot_type}.{fmt}', **fig_save_opts)
            plt.close(figs_dict[k][0])

def create_graph(adj_mat, device='gpu'):
    if device == 'gpu' and not force_use_cpu:
        graphDf = cudf.DataFrame()
        graphDf['source'] = cudf.Series(adj_mat.row)
        graphDf['destination'] = cudf.Series(adj_mat.col)

        graph = cugraph.Graph(directed=True)
        graph.from_cudf_edgelist(graphDf)
    else:
        graph = nx.from_scipy_sparse_array(adj_mat, create_using=nx.DiGraph())

    return graph

def main():
    # TODO: add as parameters
    init_values = [0.999, 0.437, 0.437, 0.484]
    kron_times = 5
    supported_plots = ['kde','hist-line','hist','kde_hist','graph','spy']

    # different options for plotting
    # kde, hist_line, hist, kde_hist, graph, spy
    # only kde and hist_line plot multiple plots on the same figure

    parser = argparse.ArgumentParser()


    parser.add_argument('--i', type=str, default='snap_graphs/ca-HepPh.txt')
    parser.add_argument('--p', metavar='P', nargs=4, type=float_range, required=False, help='Initiator probability matrix')
    parser.add_argument('--plots', metavar='F', nargs='+', help='type of plot (kde, hist-line, hist, kde_hist, graph, spy)', choices=supported_plots, default=[])
    parser.add_argument('--props', metavar='Pr', nargs='+', choices=disp_name.keys(), help='Graph properties to calculate and plot', default=[])
    parser.add_argument('--outdir', type=str, default='./plotRepo', help='Output directory for the plots')
    parser.add_argument('--from_disk', type=str, default='', help='Path to load calculated graph properties vectors')
    parser.add_argument('--gpu', action='store_true', help='Use GPU for graph operations')
    parser.add_argument('--k', type=int, help='Kronecker Power')
    args = parser.parse_args()


    # Read the real snap graph
    real_graph = None
    num_nodes = 0
    kron_times = args.k

    load_from_file = True if args.from_disk != '' else False
    if not load_from_file:
        kron_times = args.k 
        num_nodes = math.pow(2, kron_times)
        '''
        if args.gpu and not force_use_cpu:
            print(f'Reading on GPU...')
            gdf = cudf.read_csv(args.i, sep='\t', comment='#', names=['source','destination'])
            real_graph = cugraph.Graph(directed=True)
            real_graph.from_cudf_edgelist(gdf)
            num_nodes = real_graph.number_of_nodes()
        else:
            print(f'Reading on CPU...')
            real_graph = snap.LoadEdgeList(snap.TNGraph, args.i, 0, 1)
            num_nodes = real_graph.GetNodes()
            real_graph = snap_to_nx(real_graph)
        
        kron_times = math.ceil(math.log2(num_nodes))
        '''
    init_values = args.p

    if (load_from_file):
        init_values, kron_times, num_nodes = loadInfo(args.from_disk)



    print(f'Initiator Matrix: {init_values}')
    print(f'Kronecker Power: {kron_times}')
    print(f'Number of Nodes (real graph) : {num_nodes}')
    print(f'Requested Plots: {args.plots}')
    print(f'Output Directory: {args.outdir}')

    if (not os.path.exists(args.outdir)):
        os.makedirs(args.outdir)
        print(f'Directory created')
    else:
        print(f'Directory already exists')


    plots = {}
    props = {}
    for plot in args.plots:
        plots[plot] = True
    for prop in args.props:
        props[prop] = True

    # Calculate the original graph stuff
    device = 'gpu' if args.gpu else 'cpu'
    if load_from_file:
        vectors_orig = loadData(args.from_disk,-1,-1)
    '''
    else:
        vectors_orig = calcProps(real_graph, props,device)
        dumpData(vectors_orig, f'k{kron_times}_real', args.outdir)
    '''

    for i, val in enumerate(init_values):
        kde_fig_axis = {}
        with_noise_kde_fig_axis = {}
        hist_line_fig_axis = {}
        line_fig_axis = {}
        with_noise_line_fig_axis = {}
        diameters = []
        avg_shortest_path_lengths = []
        xs = []

        for prop in props.keys():
            if prop in ['hop-count','scree']:
                line_fig_axis[prop] = [None, None]
                with_noise_line_fig_axis[prop] = [None, None]
            elif prop in ['avg-shortest-path-length', 'diameter']:
                print('scalars')
            else:
                if plots.get('kde', False):
                    kde_fig_axis[prop] = [None, None]
                    with_noise_kde_fig_axis[prop] = [None, None]
                if plots.get('hist-line', False):
                    hist_line_fig_axis[prop] = [None, None]



        for graph_prop in kde_fig_axis.keys():
            kde_fig_axis[graph_prop] = list(plt.subplots())
            with_noise_kde_fig_axis[graph_prop] = list(plt.subplots())


        for graph_prop in hist_line_fig_axis.keys():
            hist_line_fig_axis[graph_prop] = list(plt.subplots())

        for graph_prop in line_fig_axis.keys():
            line_fig_axis[graph_prop] = list(plt.subplots())
            with_noise_line_fig_axis[graph_prop] = list(plt.subplots())

        new_init = init_values.copy()

        for j in range(6):
            scalars = {}

            star=''
            if j == 0:
                star='*'
                if i == 0:
                    noiseAnalysis = True
                    if (not os.path.exists(f'{args.outdir}/noise')):
                        os.makedirs(f'{args.outdir}/noise')
                        print(f'Noise Analysis directory created')
                    else:
                        print(f'Noise Analysis directory  already exists')
            else:
                new_init[i] = new_init[i] - 0.1 if i == 0 else new_init[i] + 0.1

            xs.append(new_init[i])

            names_suffix = f'x{i}_{new_init[i]:.3f}{star}'
            label = names_suffix.replace('_','=')
            names_suffix = f'k{kron_times}_{names_suffix}'

            if load_from_file:

                vectors = loadData(args.from_disk,i,j,init_values.copy())

                if noiseAnalysis:
                    alpha = 0.005
                    for ni in range(6):
                        if ni == 0:
                            n_label = 'original synthetic'
                            doPlot(plots, vectors, ni, with_noise_kde_fig_axis, {}, {}, n_label, f'{args.outdir}/noise', 'original_synthetic')
                        else:
                            n_label = f'alpha={alpha}'
                            with_noise_vectors = loadNoise(args.from_disk, alpha)
                            doPlot(plots, with_noise_vectors, ni, with_noise_kde_fig_axis, {}, {} , n_label, f'{args.outdir}/noise',f'alpha_{alpha}')
                        alpha *= 2
                    finalize_acc_plot(with_noise_kde_fig_axis, -1, kron_times, 'kde', f'{args.outdir}/noise')
                    noiseAnalysis = False
            else:
                init_Mat = Initiator(new_init)

                adj_mat = kront(init_Mat,kron_times).tocoo()


                adj_mat = mask(adj_mat)

                graph = create_graph(adj_mat, device)

                vectors = calcProps(graph, props,device)

                dumpData(vectors, names_suffix, args.outdir)

                if noiseAnalysis:
                    alpha = 0.005
                    if (args.gpu):
                        base_adj_mat = cp.sparse.coo_matrix(adj_mat)
                    else:
                        base_adj_mat = adj_mat
                    rows, cols = base_adj_mat.shape
                    for ni in range(6):
                        if ni == 0:
                            n_label = 'original synthetic'
                            doPlot(plots, vectors, ni, with_noise_kde_fig_axis, {}, {}, n_label, f'{args.outdir}/noise', 'original_synthetic')
                        else:
                            label = f'alpha={alpha}'
                            noise = RandMat([rows, cols],alpha).gen(device)
                            new_adj = (base_adj_mat + noise).tocoo()
                            with_noise_graph = create_graph(new_adj, device)
                            with_noise_vectors = calcProps(with_noise_graph, props, device)
                            dumpData(with_noise_vectors, f'noise_{alpha}', f'{args.outdir}/noise')
                            doPlot(plots, with_noise_vectors, ni, with_noise_kde_fig_axis, with_noise_line_fig_axis, {}, n_label, f'{args.outdir}/noise', f'alpha_{alpha}')
                        alpha *= 2

                    finalize_acc_plot(with_noise_kde_fig_axis,-1, kron_times,'kde', f'{args.outdir}/noise')
                    finalize_acc_plot(with_noise_line_fig_axis, -1, kron_times, 'line', f'{args.outdir}/noise')
                    noiseAnalysis = False

                print(graph)


            doPlot(plots, vectors, j, kde_fig_axis, line_fig_axis, hist_line_fig_axis, label, args.outdir, names_suffix)


            # Issues with the following, check back later
            '''

            if props.get('diameter', False):
                try:
                    diameters.append(nx.diameter(graph.to_undirected()))
                except:
                    diameters.append(10000000)

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

            if props.get('avg-shortest-path-length', False):
                try:
                    avg_shortest_path_lengths.append(nx.average_shortest_path_length(graph.to_undirected()))
                except:
                    avg_shortest_path_lengths.append(10000)
            '''
        # Plot original graph stuff
        '''
        if plots.get('kde', False):
            for graph_prop in kde_fig_axis.keys():
                plotKde(vectors_orig[graph_prop], kde_fig_axis[graph_prop][1],-1, label='real')

        if props.get('scree', False):
            plotLine(vectors_orig['scree']['x'], vectors_orig['scree']['y'], line_fig_axis['scree'][1], label='real')
        '''
        # COMMENT OUT PLOTTING THE REAL GRAPH STUFF

        '''
        names_suffix = f'k{kron_times}_real'
        

       
        doPlot(plots, vectors_orig, -1, kde_fig_axis, line_fig_axis, hist_line_fig_axis, 'real', args.outdir, names_suffix)

        '''

        finalize_acc_plot(kde_fig_axis,i, kron_times,'kde', args.outdir)
        finalize_acc_plot(hist_line_fig_axis,i, kron_times, 'hist_line', args.outdir)
        finalize_acc_plot(line_fig_axis, i, kron_times, 'line', args.outdir)
        '''
        if props.get('diameter', False):
            plotScalar(xs,diameters,f'x{i}','Diameter',f'{args.outdir}/k{kron_times}_x{i}_diameter')

        if props.get('avg-shortest-path-length', False):
            plotScalar(xs,avg_shortest_path_lengths,f'x{i}', 'Avg. Shortest Path Length',f'{args.outdir}/k{kron_times}_x{i}_avg-shortest-path-length')
        '''

    # Dump info about this run
    if not load_from_file:
        with open(f'{args.outdir}/data/info', 'w') as f:
            f.write(f"""{':'.join([str(x) for x in init_values])}\n""")
            f.write(f'k:{kron_times}\n')
            f.write(f'nodes:{num_nodes}\n')

main()

