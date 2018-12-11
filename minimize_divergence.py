HUMAN_PATH = 'study_data.json'
IMAGE_PATH = 'sravya_data.json'
TEXT_PATH


def get_alpha(text, image, human):
    # D(human | image + text)
    def fun(a):
        s = 0
        for i, key in enumerate(human.keys()):
            s += human[key]*np.log(human[key])
            s -= human[key]*np.log(text[key]*a+image[key]*(1-a))
        return s
    reutrn scipy.optimize.minimize(fun, .5)
    

def get_human():




