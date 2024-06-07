import cv2
import numpy as np



class ComparePic:

    # 输入灰度图，返回hash
    def getHash(self, image):
        avreage = np.mean(image)  # 计算进行灰度处理后图片的所有像素点的平均值， mean()函数功能：求取均值
        hash0 = []
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):  # 像素的灰度与平均值进行比较，大于或等于平均值记为1，小于记为0。
                if image[i, j] > avreage:
                    hash0.append(1)
                else:
                    hash0.append(0)

        return hash0

    # 计算汉明距离，对比哈希中有多少位不一样。
    # 输出值等于0说明两张图片一致，输出值不为0，则越接近0则越相似
    def Hamming_distance(self, hash1, hash2):
        num = 0
        for index in range(len(hash1)):
            if hash1[index] != hash2[index]:
                num += 1
        return num

    # 计算两个图片是否相似,输出值等于0说明两张图片一致，输出值不为0，则越接近0则越相似
    def classify_aHash(self, img1, img2):
        '''
        :param img1: 图片1路径（路径不能有中文）
        :param img2: 图片2路径（路径不能有中文）
        :return:
        '''
        image1 = cv2.imread(img1)  # cv2.imread
        image2 = cv2.imread(img2)
        # 将图片缩小到8 * 8的大小，这样做可以去除图片的细节，只保留结构和明暗等基本信息，同时摒弃不同尺寸和比例带来的图片差异。
        image1 = cv2.resize(image1, (80, 80))
        image2 = cv2.resize(image2, (80, 80))
        # 使用色彩空间转化函数 cv2.cvtColor( )进行色彩空间的转换，把缩小后的图片转化为64级灰度图（每个像素只有64种颜色）。
        gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)  # 将BGR格式转换成灰度图片
        gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
        hash1 = self.getHash(gray1)
        hash2 = self.getHash(gray2)
        return self.Hamming_distance(hash1, hash2)


if __name__ == '__main__':
    w = ComparePic()
    # 导入1.png图片和2.png图片
    img1 = r'D:\software_git\YQ-IntreHomeAppAutoTest\YQ-AndroidAppAutoTest-Canny\data\ele_screenshots\after.png'
    img2 = r'D:\software_git\YQ-IntreHomeAppAutoTest\YQ-AndroidAppAutoTest-Canny\data\ele_screenshots\before.png'
    image1 = cv2.imread(img1)
    degree = w.classify_aHash(img1, img2)
    # 输出值等于0说明两张图片一致，输出值不为0，则越接近0则越相似
    print(degree)