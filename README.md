# Generative Art In Python: Close Packed Circles

I've been creating a lot of "generative art" recently (mainly using Python), and lately I've wanted to be able to generate circles - potentially hundreds of them at random - which would *not overlap* with each other. This seems like a trivial problem at first, but like most programming problems that initially seem trivial, this was actually kind of a tricky problem to solve. My solution is documented here.

If you want to follow my art (and also gawk at some old food pics) you can check me out on instagram  [@brian_gawlik](https://www.instagram.com/brian_gawlik/?hl=en).

<p style="text-align:center">
   <img src="https://github.com/gaw1ik/Method-for-creating-image-with-non-overlapping-circles/blob/master/test1.gif" width="32%"/>
   <img src="https://github.com/gaw1ik/Method-for-creating-image-with-non-overlapping-circles/blob/master/test2.png" width="32%"/>
   <img src="https://github.com/gaw1ik/Method-for-creating-image-with-non-overlapping-circles/blob/master/test2.gif" width="32%"/> 
   <img src="https://github.com/gaw1ik/Method-for-creating-image-with-non-overlapping-circles/blob/master/test3.png" width="32%"/> 
   <img src="https://github.com/gaw1ik/Method-for-creating-image-with-non-overlapping-circles/blob/master/test3.gif" width="32%"/> 
   <img src="https://github.com/gaw1ik/Method-for-creating-image-with-non-overlapping-circles/blob/master/test4.png" width="32%"/> 
</p>

# Description of Algorithm
The GIFs above provide a visual for how the algorithm works, and the still images show some examples of the intended artistic output. First, an initial circle is placed at random with radius equal to the biggest desirable radius (specified in the Inputs section). Then one-by-one, additional circles are placed at random *in the remaining available space* in the frame (areas not yet covered by a circle). An image mask can be used here to dictate the available space, confining the circles to arbitrary regions (as is done in the static png examples above). These circles are initially given the smallest desirable radius (also specified in the Inputs), and then their radius is increased gradually, until they "bump" into any existing circles (the **bump condition**), at which point the image created in the previous iteration is recorded and the process is repeated until the **stop condition** is met.

The two conditions are defined as follows:

### The "Bump" Condition:
The "bump" condition is defined as when (nRegions < nCircles). 

Where:

*nRegions = # of image regions (AKA segments) as calculated using skimage.measure.regionprops*

*nCircles = # of circles currently placed in the frame which are tallied as the code iterates*

When the circles are not overlapping, nRegions should be equal to nCircles, because each region *is* a circle, but once there is an overlap, nRegions will be less than nCircles, because at that point, multiple circles are contributing to the same region.

### The Stop Condition:
The number of failed attempts to create a new circle are tallied during each iteration. Failed attempts happen when the initial placement of a circle overlaps with existing circles. When the number of failed attempts exceeds a certain number (I have used anywhere from 150 to 1000 for these examples) the program is ended. This is a fairly non-robust stop condition, but it gets the job done just fine (at least for this range of Input parameters).

# Points of Discussion
1. The code provided in this repository generates a mask (binary image) containing the closely packed circles. It should plot after being run. The script has a few inputs which allow you to adjust the size of the mask (width and height), the stop condition, the biggest and smallest desirable radii, and the seed for the random arrangement.

2. In the still images shown above, I have used the final output (the image mask containing the packed circles) as an input to another code which uses the pycairo library to draw circles of different colors. Pycairo is a graphics library for python which enables convenient illustration tools such as coloring, outlining, etc. Unlike the Skimage library, which I use for the initial mask creation, Cairo draws circles with interpolated edges. This avoids jagged edges, which are especially prevalent in smaller circles when using Skimage, and the smallest circles literally just become squares :( I digress... The location and size of the circles are dictated by the output mask based on the centroid and radius (sqrt(area/pi)) of the mask's regions (calculated using *skimage.measure.regionprops*). Also, in the generation of the packed circles mask, a separate mask containing one large center circle is used to constrain the drawing area, resulting in the packed circles forming a larger circle of their own... Cool! 

# Brief Closing Thoughts
This certainly isn't the most robust approach to this problem, and yet, I like the artistic nature of this solution. Something about it feels very organic, almost as if the algorithm is really *trying* to make itself work. The random selection and trial and error of the process makes for a great visual as well.
