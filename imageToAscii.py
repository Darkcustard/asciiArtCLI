gotlibs = False

try:
    import argparse
    import os
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

    parser.add_argument('file',metavar='file',type=str,help='Path to image or folder.')
    parser.add_argument('-o', dest='outfile', metavar='path', type=str, help='Path to output file.')
    parser.add_argument('-v', '--verbose', action='store_true', dest='verbose', help='Output logs to console.')
    parser.add_argument('-p', '--preview', action='store_true', dest='preview', help='Output image preview to console.')
    parser.add_argument('-a', '--auto', action='store_true', dest='auto', help='Auto Shift brightness values to improve detail.')
    parser.add_argument('-s', metavar='scale', default=0.01, type=float,dest='scale',help='Change scale of ASCII Image (0-1)')

    args = parser.parse_args()
    batchmode = False

    if os.path.isdir(args.file):
        batchmode = True
        print("Starting in batch mode...")

    def process(imagepath,outfile=None):

        # Generate ASCII Art
        chars = ['  ','. ' ,', ',"* ", '% ',"# ","@ "]

        if args.verbose:
            print("Loading Image...")


        raw_image = Image.open(imagepath)
        raw_image = raw_image.convert('RGB')
        
        image = np.asarray(raw_image)
        
        
        width = raw_image.width
        height = raw_image.height


        

        if args.auto:
            if args.verbose:
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
        if args.verbose:
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

        if outfile != None:
            if args.verbose:
                print(f'Saving image to {outfile}...')
            with open(outfile,'w') as f:
                f.writelines(asciiImage)



        if args.preview:
            if args.verbose:
                print('Displaying ASCII Preview...')
            print('\n'+asciiImage+'\n')
    

    if batchmode:

        if args.outfile != None:
            if os.path.isdir(args.outfile):

                for fdx,file in enumerate(sorted(os.listdir(args.file))):
                    process(args.file+file,args.outfile+str(fdx)+'.txt')
            else:
                print("ERROR: When in batch mode, outfile must be a directory")

        else:

            for file in sorted(os.listdir(args.file)):
                process(args.file+file)

    else:

        process(args.file,args.outfile)





if __name__ == "__main__" and gotlibs:
    main()
