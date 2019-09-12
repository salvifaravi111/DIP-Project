import cv2

class Image_Preprocess:
    def __init__(self):
        pass

    def read_image(self, path):
        self.path = path
        self.image_pixels = list()
        self.current_pixels = list()

        self.model_pixels = list()

        for file in path:
            img = cv2.imread(file, 0)
            self.image_pixels.append(img)
            self.current_pixels.append(img)

        print('Image Loaded')

        return self.current_pixels

    def global_threshold(self):

        try:
            for i in range(len(self.current_pixels)):
                _, self.current_pixels[i] = cv2.threshold(self.current_pixels[i], 127, 255, cv2.THRESH_BINARY)

            print('Global Threshold Applied')

            return self.current_pixels


        except Exception as e:
            print(e)

    def adaptive_mean(self):
        try:
            for i in range(len(self.current_pixels)):
                self.current_pixels[i] = cv2.adaptiveThreshold(self.current_pixels[i], 255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,11,2)

            print('Adaptive Mean Threshold Applied')

            return self.current_pixels


        except Exception as e:
            print(e)



    def adaptive_gaussian(self):
        try:
            for i in range(len(self.current_pixels)):
                self.current_pixels[i] = cv2.adaptiveThreshold(self.current_pixels[i], 255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)

            print('Adaptive Gaussian Threshold Applied')

            return self.current_pixels


        except Exception as e:
            print(e)

    def gaussian_blur(self):
        try:
            for i in range(len(self.current_pixels)):
                self.current_pixels[i] = cv2.GaussianBlur(self.current_pixels[i], (5,5) , 0)

            print('Gaussian Applied')

            return self.current_pixels


        except Exception as e:
            print(e)

    def median_blur(self):
        try:
            for i in range(len(self.current_pixels)):
                self.current_pixels[i] = cv2.medianBlur(self.current_pixels[i], 5)

            print('Median Blur Applied')

            return self.current_pixels


        except Exception as e:
            print(e)



    def get_original_image(self):
        for i in range(len(self.image_pixels)):
            self.current_pixels[i] = self.image_pixels[i]

        print('Reverted to Original Image')

        return self.current_pixels


    def model_one(self, test_path):
        print(test_path)
        self.model_pixels.clear()


        index = 0

        for path in self.path:
            print('path',index,path)
            if path != test_path:
                index += 1
            elif path == test_path:
                break

        if len(test_path) == index-1:
            raise ValueError('Not Found')

        self.model_pixels.clear()
        img2 =  self.current_pixels[index].copy()
        template = self.current_pixels[index].copy()

        box1 = img2[0:26,0:24]
        box2 = img2[26:52,24:48]
        box3 = img2[52:78,48:72]
        box4 = img2[78:104,72:96]
        boxes = [box1,box2,box3,box4]

        box1 = template[0:26,0:24]
        box2 = template[26:52,24:48]
        box3 = template[52:78,48:72]
        box4 = template[78:104,72:96]
        tboxes = [box1,box2,box3,box4]

        w, h = box1.shape[::-1]

        # All the 6 methods for comparison in a list
        methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
                    'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']


        #for meth in methods:
        for i in range(0,4):
            img = boxes[i].copy()
            method = eval(methods[0])

            # Apply template Matching
            res = cv2.matchTemplate(img,tboxes[i],method)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

            # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
            if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
                top_left = min_loc
            else:
                top_left = max_loc
            bottom_right = (top_left[0] + w, top_left[1] + h)

            backtorgb = cv2.cvtColor(img,cv2.COLOR_GRAY2RGB)
            cv2.rectangle(backtorgb,top_left, bottom_right, (255,0,0), 2)
            self.model_pixels.append(backtorgb)

        return self.model_pixels, index


    def model_two(self, test_path):

        index = 0

        for path in self.path:
            print('path',index,path)
            if path != test_path:
                index += 1
            elif path == test_path:
                break

        if len(test_path) == index-1:
            raise ValueError('Not Found')

        self.model_pixels.clear()
        img2 =  self.current_pixels[index].copy()
        template = self.current_pixels[index].copy()

        box1 = img2[0:26,0:24]
        box2 = img2[26:52,24:48]
        box3 = img2[52:78,48:72]
        box4 = img2[78:104,72:96]
        boxes = [box1,box2,box3,box4]

        box1 = template[0:26,0:24]
        box2 = template[26:52,24:48]
        box3 = template[52:78,48:72]
        box4 = template[78:104,72:96]
        tboxes = [box1,box2,box3,box4]

        w, h = box1.shape[::-1]

        # All the 6 methods for comparison in a list
        methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
                    'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']


        #for meth in methods:
        for i in range(0,4):
            img = boxes[i].copy()
            method = eval(methods[1])

            # Apply template Matching
            res = cv2.matchTemplate(img,tboxes[i],method)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

            # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
            if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
                top_left = min_loc
            else:
                top_left = max_loc
            bottom_right = (top_left[0] + w, top_left[1] + h)

            backtorgb = cv2.cvtColor(img,cv2.COLOR_GRAY2RGB)
            cv2.rectangle(backtorgb,top_left, bottom_right, (255,0,0), 2)
            self.model_pixels.append(backtorgb)

        return self.model_pixels, index

