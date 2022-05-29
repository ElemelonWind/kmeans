# kmeans

Unsupervised learning algorithm that is widely used to in applications such as Image Segmentation, Clustering Gene Segmentation Data, News Article Clustering, Clustering Languages, Species Clustering, Anomaly Detection etc. It finds the mean of groups of points and uses it to classify dataset. In this project, an image can be passed in through the command line argument as either a file path or a link, in the format of `k image`, where `k` is the number of colors (means). It will then be put through the clustering algorithm to return an image with only `k` distinct colors.

## algorithm

- Find K starting 'means' from the set of pixel values in the image using the K++ algorithm
- For each point in the set, decide which of the K means it is closest to (using the 3D distance formula), and put it in that group.
- Figure out the means of all K groups and these become the new means.
- Repeat step 2 and 3 until points stop "group hopping"

## k++

Specifies a procedure to initialize the cluster centers before proceeding with the standard k-means optimization iterations. With the k-means++ initialization, the algorithm is guaranteed to find a solution that is `O(log k)` competitive to the optimal k-means solution.

The exact algorithm is as follows:

- Choose one center uniformly at random among the data points.
- For each data point `x` not chosen yet, compute `D(x)`, the distance between x and the nearest center that has already been chosen.
- Choose one new data point at random as a new center, using a weighted probability distribution where a point `x` is chosen with probability proportional to `D(x)^2`.
- Repeat Steps 2 and 3 until `k` centers have been chosen.
- Now that the initial centers have been chosen, proceed using standard k-means clustering.

However, because I am using pixel RGB values, all I needed to do was put every pixel in a list and sort them using Python's `sorted()` method. Then, I chose `k` evenly spaced pixels in the list as my initial means.

With optimized initial means, the k-means algorithm converges much faster and obtains typically 2-fold improvements in speed; for certain datasets it achieved close to 1000-fold improvements in error.
