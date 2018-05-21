import time
import random
import sys
from PIL import Image


def main():
    if len(sys.argv) < 4:
        print('Usage: python3 dbscan.py image.bmp r min_pts')
        return
    img = Image.open(sys.argv[1])
    rgb_im = img.convert('RGB')
    dbscan(rgb_im, int(sys.argv[2]), int(sys.argv[3]))

    rgb_im.save('output.bmp')


def dbscan(rgb_im, r, min_pts):
    global k
    global color
    black_pos = []
    pixdata = rgb_im.load()
    for i in range(rgb_im.size[0]):
        for j in range(rgb_im.size[1]):
            if pixdata[i, j] == (0, 0, 0):
                black_pos.append([i, j])
    # scan all black_pixel
    state = [[False
              for i in range(rgb_im.size[0])] for j in range(rgb_im.size[1])]
    for pos in black_pos:
        if state[pos[1]][pos[0]]:
            continue
        # haven't scanned yet
        # new clustering or noise
        # scan whole circle
        new_clustering_ary = scan_circle(pos, rgb_im, pixdata, r)

        state[pos[1]][pos[0]] = True
        if len(new_clustering_ary) >= min_pts:
            # new clustering
            k += 1
            color.append((
                random.randrange(0, 256),
                random.randrange(0, 256),
                random.randrange(0, 256)))
            # paint color
            pixdata[pos[0], pos[1]] = color[k - 1]
            # clustering until empty
            while new_clustering_ary:
                pos = new_clustering_ary.pop()
                if state[pos[1]][pos[0]]:
                    continue
                pixdata[pos[0], pos[1]] = color[k - 1]
                in_circle_ary = scan_circle(pos, rgb_im, pixdata, r)
                state[pos[1]][pos[0]] = True
                if len(in_circle_ary) >= min_pts:
                    new_clustering_ary.extend(in_circle_ary)


def scan_circle(pos, rgb_im, pixdata, r):
    in_circle_ary = []

    # scan whole circle
    for i in range(pos[0] - r, pos[0] + r):
        if (i < 0) or (i >= rgb_im.size[0]):
            continue
        for j in range(pos[1] - r, pos[1] + r):
            if (j < 0) or (j >= rgb_im.size[1]):
                continue
            if pixdata[i, j] == (255, 255, 255):
                continue
            # pixel is black
            in_circle_ary.append([i, j])
    return in_circle_ary


if __name__ == '__main__':
    global k
    global color
    k = 0
    color = []
    start = time.time()
    main()
    print('clustering num:', k)
    print("it took", time.time() - start, "seconds.")
