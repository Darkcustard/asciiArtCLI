gotlibs = False

try:
    import argparse
    import numpy as np
    from PIL import Image
    gotlibs = True
except:
    print('Failed to load all libraries, check requirements.txt')



def main():

    # create argument parser
    parser = argparse.ArgumentParser(

        prog='imageToAscii',
        description='convert images to ascii art',
        
        )

    parser.add_argument('file',metavar='file',type=str,help='Path to image.')
    parser.add_argument('-o', dest='outfile', metavar='path', type=str, help='Path to output file.')
    parser.add_argument('-v', '--verbose', action='store_true', dest='verbose', help='Output image preview to console.')
    parser.add_argument('-a', '--auto', action='store_true', dest='auto', help='Auto Shift brightness values to improve detail.')
    parser.add_argument('-s', metavar='scale', default=0.01, type=float,dest='scale',help='Change scale of ASCII Image (0-1)')

    args = parser.parse_args()

    # Generate ASCII Art
    chars = ['  ','. ' ,', ',"* ", '% ',"# ","@ ","@ "]

    print("Loading Image...")
    image = np.asarray(Image.open(args.file))

    if args.auto:
        print("Generating pixel statistics...")
        total = 0
        items = 0

        for rdx,row in enumerate(image):
            if rdx % round(1/args.scale) == 0:

                for pdx,pixel in enumerate(row):
                    if pdx % round(1/args.scale) == 0:

                        brightness = sum(pixel)/3
                        total += brightness
                        items += 1

        avgBrightness = round(total/items)
        autoOffset = (255/2) - avgBrightness

    asciiImage = ''
    print("Generating ASCII...")

    for rdx,row in enumerate(image):
        
        if rdx % round(1/args.scale) == 0:
            asciiRow = ''

            for pdx,pixel in enumerate(row):

                if pdx % round(1/args.scale) == 0:

                    brightness = sum(pixel)/3

                    if args.auto:
                        brightness += autoOffset


                    if brightness > 255:
                        brightness = 255

                    index = round((len(chars)-1)*(brightness/255))
                    asciiRow += (chars[index])

            asciiImage += asciiRow+'\n'

    if args.outfile != None:
        print(f'Saving image to {args.outfile}...')
        with open(args.outfile,'w') as f:
            f.writelines(asciiImage)



    if args.verbose:
        print('Displaying ASCII Preview...\n')

        print(asciiImage)





if __name__ == "__main__" and gotlibs:
    main()