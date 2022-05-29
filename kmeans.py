''' Test cases:
6 https://cf.geekdo-images.com/imagepage/img/5lvEWGGTqWDFmJq_MaZvVD3sPuM=/fit-in/900x600/filters:no_upscale()/pic260745.jpg
10 cute_dog.jpg
6 turtle.jpg
'''
import PIL
from PIL import Image
import urllib.request
import io, sys, os, random
import tkinter as tk
from PIL import Image, ImageTk

def choose_random_means(k, img, pix):
   means = []
   while len(means) < k:
       cur = pix[random.randint(0, img.size[0]-1), random.randint(0, img.size[1]-1)]
       if cur not in means: means.append(cur)
   return means

def kpp(k, img, pix):
   li = []
   for x in range(img.size[0]):
       for y in range(img.size[1]):
           li.append(pix[x,y])
   li = sorted(li)
   dist = (len(li)-1)//(k-1)
   return [li[dist*i] for i in range(k)]

# goal test: no hopping
def check_move_count(mc):
   for c in mc:
       if c: return False
   return True

# calculate distance with the current color with each mean
# return the index of means
def dist(col, means):
   dists = {}
   for i in range(len(means)):
       cur = means[i]
       dist = sum([(cur[j]-col[j])**2 for j in range(3)])
       dists[i] = dist
   return min(dists, key=lambda key: dists[key]) 

def choose_mean(pixs):
    if len(pixs) == 0: return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) 
    avgR = sum([pix[0] for pix in pixs])/len(pixs)
    avgG = sum([pix[1] for pix in pixs])/len(pixs)
    avgB = sum([pix[2] for pix in pixs])/len(pixs)
    return (avgR, avgG, avgB)

def clustering(img, pix, cb, mc, means, count):
   temp_pb, temp_mc, temp_m = [[] for x in means], [], []
   temp_cb = [0 for x in means]
   
   for x in range(img.size[0]):
       for y in range(img.size[1]):
           ind = dist(pix[x,y], means)
           temp_pb[ind].append(pix[x,y])
           temp_cb[ind]+=1

   temp_m = [choose_mean(i) for i in temp_pb] # fix later to find actual mean formula if doesn't work

   temp_mc = [(a-b) for a, b in zip(temp_cb, cb)] # fix later to do with temp_pb if doesn't work
   print ('diff', count, ':', temp_mc)
   return temp_cb, temp_mc, temp_m

def update_picture(img, pix, means):
   region_dict = {}

   intMeans = []
   for i in range(len(means)):
       intMeans.append(tuple([int(means[i][j]) for j in range(3)]))

   for x in range(img.size[0]):
       for y in range(img.size[1]):
           ind = dist(pix[x,y], means)
           pix[x,y] = intMeans[ind]

   return pix, intMeans
   
def distinct_pix_count(img, pix):
   cols = {}
   for x in range(img.size[0]):
       for y in range(img.size[1]):
          if pix[x,y] in cols:
              cols[pix[x,y]]+=1
          else:
              cols[pix[x,y]]=1
   max_col = max(cols, key=lambda key: cols[key])
   max_count = cols[max_col]
   return len(cols.keys()), max_col, max_count

def count_regions(img, pix, means):
   rep_col = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
   while rep_col in means:
       rep_col = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
   region_count = [0 for x in means]
   bound_x = img.size[0]
   bound_y = img.size[1]
   for i in range(len(means)):
      while True: 
       cur_col = means[i]
       found_col = False
       for x in range(img.size[0]):
        for y in range(img.size[1]):
            if pix[x,y] == cur_col:
                cur_x = x 
                cur_y = y 
                found_col = True
                break
        if found_col: break 
       if not found_col: break
       region_count[i]+=1
       pix = floodfill(cur_x, cur_y, pix, cur_col, rep_col, bound_x, bound_y)
   return region_count

def floodfill(x, y, pix, color, fill_col, bound_x, bound_y):
    queue = [(x, y)]
    count = 0
    while count < len(queue):
       x, y = queue[count][0], queue[count][1]
       count+=1
       if x < 0 or x >= bound_x or y < 0 or y >= bound_y or pix[x,y] != color:
        continue 
       pix[x,y] = fill_col
       queue.append((x+1, y))
       queue.append((x, y+1))
       queue.append((x-1, y))
       queue.append((x, y-1))
       queue.append((x+1, y+1))
       queue.append((x+1, y-1))
       queue.append((x-1, y+1))
       queue.append((x-1, y-1))
    return pix
 
def main():
   k = int(sys.argv[1])
   file = sys.argv[2]
   if not os.path.isfile(file):
      file = io.BytesIO(urllib.request.urlopen(file).read())
   
   window = tk.Tk()
   
   img = Image.open(file)
   
   img_tk = ImageTk.PhotoImage(img)
   lbl = tk.Label(window, image = img_tk).pack()  
   
   pix = img.load()   # pix[0, 0] : (r, g, b) 
   print ('Size:', img.size[0], 'x', img.size[1])
   print ('Pixels:', img.size[0]*img.size[1])
   d_count, m_col, m_count = distinct_pix_count(img, pix)
   print ('Distinct pixel count:', d_count)
   print ('Most common pixel:', m_col, '=>', m_count)

   count_buckets = [0 for x in range(k)]
   move_count = [10 for x in range(k)]
   means = kpp(k, img, pix)
   print ('kpp means:', means)
   count = 1
   while not check_move_count(move_count):
      count += 1
      count_buckets, move_count, means = clustering(img, pix, count_buckets, move_count, means, count)
      if count == 2:
         print ('first means:', means)
         print ('starting sizes:', count_buckets)
   pix, intMeans = update_picture(img, pix, means)
   print ('Final sizes:', count_buckets)
   print ('Final means:')
   for i in range(len(means)):
      print (i+1, ':', means[i], '=>', count_buckets[i])
      
   img_tk1 = ImageTk.PhotoImage(img)
   lbl = tk.Label(window, image = img_tk1).pack()  # display the image at window
   
   img.save('kmeans/image.png', 'PNG')

   print('Region counts:', count_regions(img, pix, intMeans))

   window.mainloop()
   
if __name__ == '__main__': 
   main()
