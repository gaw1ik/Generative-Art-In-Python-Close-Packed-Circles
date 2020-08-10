# Method for Creating Images Containing Non-Overlapping Circles (Using Python)

<p style="text-align:center">
   <img src="https://github.com/gaw1ik/Method-for-creating-image-with-non-overlapping-circles/blob/master/test1.gif" width="32%"/>
   <img src="https://github.com/gaw1ik/Method-for-creating-image-with-non-overlapping-circles/blob/master/test2.gif" width="32%"/> 
   <img src="https://github.com/gaw1ik/Method-for-creating-image-with-non-overlapping-circles/blob/master/test3.gif" width="32%"/> 
</p>

# Background
Along my journey writing programs for generative art, I realized I wanted to be able to generate circles - potentially hundreds of them at random - which would not overlap with each other. This seems like a trivial problem at first, but like most programming problems that initially seem trivial, this was actually kind of a tricky problem to solve. My solution is documented here.

# Description of Algorithm
The GIFs above provides a visual for how the algorithm works. First, an initial circle is placed at random with radius equal to the desired initial radius (specified in the Inputs section). Then one-by-one, additional circles are placed at random *in the remaining available space* in the frame (areas not yet covered by a circle). These circles are initially given the smallest desirable radius (also specified in the Inputs), and then their radius is increased gradually, until they "bump" into any existing circles (the **bump condition**), at which point the image created in the previous iteration is recorded and the process is repeated until the **stop condition** is met.

The two conditions are defined as follows:

### The "Bump" Condition:
The "bump" condition is defined as when (nRegions < nCircles). 

Where:

*nRegions = # of image regions (AKA segments)*

*nCircles = # of circles currently placed in the frame*

When the cirlces are not overlapping, nRegions should be equal to nCircles, because each region *is* a circle, but once there is an overlap, nRegions will be less than nCircles, because at that point, multiple circles are contributing to the same region.

### The Stop Condition:
The number of failed attempts to create a new circle are tallied during each iteration. Failed attempts happen when the initial placement of a circle overlaps with existing circles. When the number of failed attempts exceed a certain number (I have used anywhere from 150 to 1000 for these examples) the program is ended. This is a fairly non-robust stop condition, but it gets the job done just fine (at least for this range of Input parameters).

# Brief Closing Thoughts
This certainly isn't the most robust approach to this problem, and yet, I like the artistic nature of this solution. Something about it feels very organic, almost as if the algorithm is really *trying* to make itself work. The random selection and trial and error of the process makes for a great visual as well.
