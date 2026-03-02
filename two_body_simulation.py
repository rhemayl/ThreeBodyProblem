import time
import scipy as sci
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("Agg")
from matplotlib import animation
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def twobp(position, velocity, mass1, mass2, video_path):
    
    plt.style.use('dark_background')
    T1 = time.time()

    #d: dynamic framing
    #a: autoscaling
    #c: constant frame
    FRAMING_METHOD = "c"
    
    #MARKER_COLORS = ("darkblue", "darkred")
    MARKER_COLORS = ("darkturquoise", "mediumorchid")
    #TRACE_COLORS = ("mediumblue", "red")
    TRACE_COLORS = ("cyan", "fuchsia")

    # Non-Dimensionalisation
    G=6.67408e-11 #N-m2/kg2

    #Reference quantities
    m_nd=1.989e+30 #kg
    r_nd=5.326e+12 #m
    v_nd=30000 #m/s
    t_nd=79.91*365.25*24*3600 #s

    #Net constants
    K1=G*t_nd*m_nd/(r_nd**2*v_nd)
    K2=v_nd*t_nd/r_nd

    #Define masses
    #m1=G #Star 1
    #m2=G #Star 2
    #m3=G #Star 3

    if mass1:
        m1 = float(mass1)
    else: 
        m1=1.1 
    if mass2:
        m2 = float(mass2)
    else: 
        m2=0.907

    #r1 = input("set body 1 starting position (x,y,z): ").split(",")
    #r2 = input("set body 2 starting position (x,y,z): ").split(",")
    #r3 = input("set body 3 starting position (x,y,z): ").split(",")

    #Convert pos vectors to arrays
    if len(position) == 11:
        position = position.split(",")
        try:
            position = [float(n) for n in position]
            r1=position[0:3]
            r2=position[3:6]
        except:
            return "Please enter exactly 6 comma-separated numbers."
    elif len(position) == 0:
        #Define initial position vectors
        r1=[-0.5,1,0] #m
        r2=[0.5,0,0.5] #m
    else:
        return "Please enter exactly 6 comma-separated numbers."

    r1=np.array(r1)
    r2=np.array(r2)

    #Find Centre of Mass
    r_com=(m1*r1+m2*r2)/(m1+m2)

    #Define initial velocities

    #V1 = 0.412103
    #V2 = 0.283384

    #v1=[V1,V2,0] #m/s
    #v2=[V1,V2,0] #m/s
    #v3=[-2*V1,--2*V2,0]

    if len(velocity) == 11:
        velocity = velocity.split(",")
        try:
            velocity = [float(n) for n in velocity]
            v1=velocity[0:3]
            v2=velocity[3:6]
        except:
            return "Please enter exactly 9 comma-separated numbers."
    elif len(velocity) == 0:
        v1=[0.02,0.02,0.02] #m/s
        v2=[-0.05,0,-0.1] #m/s
    else:
        return "Please enter exactly 9 comma-separated numbers."

    #Convert velocity vectors to arrays
    v1=np.array(v1)
    v2=np.array(v2)

    #Find velocity of COM
    v_com=(m1*v1+m2*v2)/(m1+m2)

    def ThreeBodyEquations(w,t,G,m1,m2):
        # Unpack variables
        r1 = w[0:3]
        r2 = w[3:6]
        v1 = w[6:9]
        v2 = w[9:12]

        # Separation vector and distance (protect against singular)
        r12_vec = r2 - r1
        eps = 1e-12
        r12 = np.linalg.norm(r12_vec)
        inv_r12_3 = 1.0 / (r12**3 + eps)

        # Accelerations
        dv1bydt = K1 * (m2 * r12_vec * inv_r12_3)
        dv2bydt = K1 * (m1 * (-r12_vec) * inv_r12_3)

        # Position derivatives
        dr1bydt = K2 * v1
        dr2bydt = K2 * v2

        # Package derivatives into preallocated array to avoid concatenations
        derivs = np.empty(12, dtype=float)
        derivs[0:3] = dr1bydt
        derivs[3:6] = dr2bydt
        derivs[6:9] = dv1bydt
        derivs[9:12] = dv2bydt
        return derivs

    HOW_LONG = 10 #seconds
    #Package initial parameters
    init_params=np.array([r1,r2,v1,v2]) #Package initial parameters into one size-12 array
    init_params=init_params.flatten() #Flatten the array to make it 1D
    time_span=np.linspace(0,2*HOW_LONG,100*HOW_LONG) #Time span is 20 orbital years and 1000 points


    #Run the ODE solver
    three_body_sol=sci.integrate.odeint(ThreeBodyEquations,init_params,time_span,args=(G,m1,m2))


    #Store the position solutions into three distinct arrays
    r1_sol=three_body_sol[:,:3]
    r2_sol=three_body_sol[:,3:6]


    # Compute marker sizes once (avoid building a separate static figure)
    mmin = min(m1, m2)

    s1 = 60 * m1 / mmin
    s2 = 60 * m2 / mmin


    #Animate the orbits of the three bodies


    #Make the figure 
    fig=plt.figure(figsize=(15,15))
    ax=fig.add_subplot(111,projection="3d")

    #Create new arrays for animation, this gives you the flexibility
    #to reduce the number of points in the animation if it becomes slow
    #Currently set to select every 4th point
    stride = 1
    r1_sol_anim=r1_sol[::stride,:].copy()
    r2_sol_anim=r2_sol[::stride,:].copy()

    #Set initial marker for planets, that is, blue,red and green circles at the initial positions
    #head1=[ax.scatter(r1_sol_anim[0,0],r1_sol_anim[0,1],r1_sol_anim[0,2],color=MARKER_COLORS[0],marker="o",s=80,label="Star 1")]
    #head2=[ax.scatter(r2_sol_anim[0,0],r2_sol_anim[0,1],r2_sol_anim[0,2],color=MARKER_COLORS[1],marker="o",s=80,label="Star 2")]
    #head3=[ax.scatter(r3_sol_anim[0,0],r3_sol_anim[0,1],r3_sol_anim[0,2],color="darkgreen",marker="o",s=80,label="Star 3")]
    
    head1=ax.scatter([],[],[],color=MARKER_COLORS[0],marker="o",s=s1,label="Star 1")
    head2=ax.scatter([],[],[],color=MARKER_COLORS[1],marker="o",s=s2,label="Star 2")

    trace1, = ax.plot([], [], [], color = TRACE_COLORS[0])
    trace2, = ax.plot([], [], [], color = TRACE_COLORS[1])
    #Create a function Animate that changes plots every frame (here "i" is the frame number)
    
    SCALING_WINDOW = 100     # frames to consider
    SCALING_PADDING = 0.3
    def Animate(i,head1,head2):
        #Remove old markers
        #head1[0].remove()
        #head2[0].remove()
        #head3[0].remove()

        #Plot the orbits (every iteration we plot from initial position to the current position)
        #trace1=ax.plot(r1_sol_anim[:i,0],r1_sol_anim[:i,1],r1_sol_anim[:i,2],color=TRACE_COLORS[0])
        #trace2=ax.plot(r2_sol_anim[:i,0],r2_sol_anim[:i,1],r2_sol_anim[:i,2],color=TRACE_COLORS[1])
        #trace3=ax.plot(r3_sol_anim[:i,0],r3_sol_anim[:i,1],r3_sol_anim[:i,2],color="green")

        #Plot the current markers
        #head1[0]=ax.scatter(r1_sol_anim[i-1,0],r1_sol_anim[i-1,1],r1_sol_anim[i-1,2],color=MARKER_COLORS[0],marker="o",s=100)
        #head2[0]=ax.scatter(r2_sol_anim[i-1,0],r2_sol_anim[i-1,1],r2_sol_anim[i-1,2],color=MARKER_COLORS[1],marker="o",s=100)
        #head3[0]=ax.scatter(r3_sol_anim[i-1,0],r3_sol_anim[i-1,1],r3_sol_anim[i-1,2],color="darkgreen",marker="o",s=100)
        trace1.set_data(r1_sol_anim[:i,0], r1_sol_anim[:i,1])
        trace1.set_3d_properties(r1_sol_anim[:i,2])
        trace2.set_data(r2_sol_anim[:i,0], r2_sol_anim[:i,1])
        trace2.set_3d_properties(r2_sol_anim[:i,2])

        head1._offsets3d = (
            [r1_sol_anim[i,0]],
            [r1_sol_anim[i,1]],
            [r1_sol_anim[i,2]]
        )
        head2._offsets3d = (
            [r2_sol_anim[i,0]],
            [r2_sol_anim[i,1]],
            [r2_sol_anim[i,2]])
        
        if FRAMING_METHOD == "d":
            start = max(0, i - SCALING_WINDOW)
            xs = np.concatenate([
            r1_sol_anim[start:i+1,0],
            r2_sol_anim[start:i+1,0],
            ])
            ys = np.concatenate([
                r1_sol_anim[start:i+1,1],
                r2_sol_anim[start:i+1,1],
            ])
            zs = np.concatenate([
                r1_sol_anim[start:i+1,2],
                r2_sol_anim[start:i+1,2],
            ])

            ax.set_xlim(xs.min()*(1-SCALING_PADDING), xs.max()*(1+SCALING_PADDING))
            ax.set_ylim(ys.min()*(1-SCALING_PADDING), ys.max()*(1+SCALING_PADDING))
            ax.set_zlim(zs.min()*(1-SCALING_PADDING), zs.max()*(1+SCALING_PADDING))
        elif FRAMING_METHOD == "a":
            ax.autoscale_view()
        
        return trace1,trace2,head1,head2

    #Some beautifying
    ax.xaxis.set_pane_color((0, 0, 0, 0))
    ax.yaxis.set_pane_color((0, 0, 0, 0))
    ax.zaxis.set_pane_color((0, 0, 0, 0))
    ax.set_xlabel("x-coordinate",fontsize=14)
    ax.set_ylabel("y-coordinate",fontsize=14)
    ax.set_zlabel("z-coordinate",fontsize=14)
    ax.set_title("Visualization of orbits of stars in a 2-body system\n",fontsize=14)
    ax.legend(loc="upper left",fontsize=14)


    #If used in Jupyter Notebook, animation will not display only a static image will display with this command
    # anim_2b = animation.FuncAnimation(fig,Animate_2b,frames=1000,interval=5,repeat=False,blit=False,fargs=(h1,h2))

    # PADDING APPROACH
    r_com_sol = (m1*r1_sol_anim + m2*r2_sol_anim) / (m1 + m2)

    r1c = r1_sol_anim - r_com_sol
    r2c = r2_sol_anim - r_com_sol

    if FRAMING_METHOD == "c":
        
        all_x = np.concatenate((r1_sol_anim[:,0], r2_sol_anim[:,0]))
        all_y = np.concatenate((r1_sol_anim[:,1], r2_sol_anim[:,1]))
        all_z = np.concatenate((r1_sol_anim[:,2], r2_sol_anim[:,2]))

        #pad = 0.2  # PADDING factor
        #ax.set_xlim(all_x.min()*(1+pad), all_x.max()*(1+pad))
        #ax.set_ylim(all_y.min()*(1+pad), all_y.max()*(1+pad))
        #ax.set_zlim(all_z.min()*(1+pad), all_z.max()*(1+pad))

        #low, high = 2, 98   # percentiles
        #pad = 0.2
#
        #xmin, xmax = np.percentile(all_x, [low, high])
        #ymin, ymax = np.percentile(all_y, [low, high])
        #zmin, zmax = np.percentile(all_z, [low, high])
#
        #ax.set_xlim(xmin*(1-pad), xmax*(1+pad))
        #ax.set_ylim(ymin*(1-pad), ymax*(1+pad))
        #ax.set_zlim(zmin*(1-pad), zmax*(1+pad))

        #Distances from center of mass
        d1 = np.linalg.norm(r1_sol_anim - r_com_sol, axis=1)
        d2 = np.linalg.norm(r2_sol_anim - r_com_sol, axis=1)

        # Robust extent: ignore extreme outliers
        max_extent = np.percentile(
            np.concatenate([d1, d2]),
            95
        )
        pad = 1.2
        L = max_extent * pad

        ax.set_xlim(-L, L)
        ax.set_ylim(-L, L)
        ax.set_zlim(-L, L)

        ax.set_box_aspect((1, 1, 1))

        #Method 2
        #all_x = np.concatenate([r1c[:,0], r2c[:,0]])
        #all_y = np.concatenate([r1c[:,1], r2c[:,1]])
        #all_z = np.concatenate([r1c[:,2], r2c[:,2]])
#
        #mavg = (m1 + m2) / 2
        #dm1, dm2 = abs(m1 - mavg), abs(m2 - mavg)
        #maxdm = max(dm1, dm2) / 0.2
        #low, high = maxdm, 100-maxdm   # tighten if needed
        #pad = 1.2
#
        #xmin, xmax = np.percentile(all_x, [low, high])
        #ymin, ymax = np.percentile(all_y, [low, high])
        #zmin, zmax = np.percentile(all_z, [low, high])
#
        #ax.set_xlim(xmin*pad, xmax*pad)
        #ax.set_ylim(ymin*pad, ymax*pad)
        #ax.set_zlim(zmin*pad, zmax*pad)
#
        #ax.set_box_aspect((1, 1, 1))

    #Use the FuncAnimation module to make the animation
    repeatanim=animation.FuncAnimation(fig,Animate,frames=30*HOW_LONG,interval=10,repeat=False,blit=False,fargs=(head1,head2))

    # Set up formatting for the movie files
    Writer = animation.writers['ffmpeg']
    writer = Writer(fps=30, metadata=dict(artist='Me'), bitrate=2000)

    print("DEBUG: Finished solving ODE. Now plotting...")
    #To save animation to disk, enable this command


    repeatanim.save(video_path, writer=writer)
    T2 = time.time()
    print(f"DEBUG: Time taken: {round(T2-T1, 3)}s")

    return "Simulation Loaded!"

if __name__ == "__main__":
    twobp("", "", None, None, "test_videos/TempTwoBodyProblem.mp4")
