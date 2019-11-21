import algs
from matplotlib import pyplot as plt
import numpy as np

# def upgrade_decor(func):
#     def inner(*args, **kwargs):
#         ax, routes = args
#         if route[0]["route_improvement"] == '':
#         return func(*args, **kwargs)
#     return inner


def ax_populate(ax, routes, key):
    for route in routes:
        if key == 'initial':
            if route[0]["route_improvement"] == '':
                # start_lng, eng_lng, start_lat, end_lat
                ax.plot([route[0]['start_location_lng'],route[0]['end_location_lng']],
                        [route[0]['start_location_lat'],route[0]['end_location_lat']],
                        'ro-', linewidth=0.5, markersize=2)
            else:
                ax.plot([route[0]['start_location_lng'],route[0]['intermediate_location_lng']],
                    [route[0]['start_location_lat'],route[0]['intermediate_location_lat']],
                    'bo-', linewidth=0.8, markersize=2)
                ax.plot([route[0]['intermediate_location_lng'],route[0]['end_location_lng']],
                    [route[0]['intermediate_location_lat'],route[0]['end_location_lat']],
                    'bo-', linewidth=0.8, markersize=2)
        elif key == 'upgrated':
            ax.plot([route[0]['start_location_lng'],route[0]['end_location_lng']],
                [route[0]['start_location_lat'],route[0]['end_location_lat']],
                'ro-', linewidth=0.5, markersize=2)


def draw_initial(routes, key): # key == initial, == upgrated
    get_num_of_vert = len([route[0]['start_address'] for route in routes])
    # c = np.random.randint(1,5,size=138) # color 1 to 4 for each
    c = np.random.randint(1, 5, size=get_num_of_vert)
    norm = plt.Normalize(1, 4)
    cmap = plt.cm.RdYlGn
    fig,ax = plt.subplots()

    all_points_x = [route[0]['start_location_lng'] for route in routes] # change to 45 == # [route['end_location_lng'] for route in routes[0:get_num_of_vert]]
    all_points_y = [route[0]['start_location_lat'] for route in routes] # change to 45 == # [route['end_location_lat'] for route in routes[0:get_num_of_vert]]
    all_points_names = [route[0]['start_address'] for route in routes] # change to 45 == # [route['end_address'] for route in routes[0:get_num_of_vert]]

    ax_populate(ax, routes, key)

    sc = plt.scatter(all_points_x, all_points_y, c=None, s=100, cmap=cmap, norm=norm)

    annot = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
                        bbox=dict(boxstyle="round", fc="w"),
                        arrowprops=dict(arrowstyle="->"))
    annot.set_visible(False)


    def update_annot(ind):
        pos = sc.get_offsets()[ind["ind"][0]]
        annot.xy = pos
        text = "{}".format(" ".join([all_points_names[n] for n in ind["ind"]]))
        annot.set_text(text)
        annot.get_bbox_patch().set_facecolor(cmap(norm(c[ind["ind"][0]])))
        annot.get_bbox_patch().set_alpha(0.4)

    def hover(event):
        vis = annot.get_visible()
        if event.inaxes == ax:
            cont, ind = sc.contains(event)
            if cont:
                update_annot(ind)
                annot.set_visible(True)
                fig.canvas.draw_idle()
            else:
                if vis:
                    annot.set_visible(False)
                    fig.canvas.draw_idle()

    fig.canvas.mpl_connect("motion_notify_event", hover)

    plt.show()

def main():

    initial_routes = algs.read_uprgated_routes()
    
    draw_initial(initial_routes, key='initial')

    draw_initial(initial_routes, key='upgrated')

if __name__ == '__main__':
    main() 
