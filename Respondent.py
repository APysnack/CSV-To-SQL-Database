class Respondent(object):

    # Constructor for creating a new Respondent
    def __init__(self, rid, biacromial_di, biiliac_di, bitrochanteric_di, chest_depth, chest_di, elbow_di, wrist_di,
                 knee_di, ankle_di, shoulder_gir, chest_gir, waist_gir, navel_gir, hip_gir, thigh_gir,
                 bicep_gir, forearm_gir, knee_gir, calf_gir, ankle_gir, wrist_gir, age, weight, height, gender):

        self.rid = rid
        self.biacromial_di = biacromial_di
        self.biiliac_di = biiliac_di
        self.bitrochanteric_di = bitrochanteric_di
        self.chest_depth = chest_depth
        self.chest_di = chest_di
        self.elbow_di = elbow_di
        self.wrist_di = wrist_di
        self.knee_di = knee_di
        self.ankle_di = ankle_di
        self.shoulder_gir = shoulder_gir
        self.chest_gir = chest_gir
        self.waist_gir = waist_gir
        self.navel_gir = navel_gir
        self.hip_gir = hip_gir
        self.thigh_gir = thigh_gir
        self.bicep_gir = bicep_gir
        self.forearm_gir = forearm_gir
        self.knee_gir = knee_gir
        self.calf_gir = calf_gir
        self.ankle_gir = ankle_gir
        self.wrist_gir = wrist_gir
        self.age = age
        self.weight = weight
        self.height = height
        self.gender = gender

#-----------------------------------------------------------------------------------------#

    # list of "getters"

    @property
    def gender(self):
        return self._gender

    @property
    def rid(self):
        return self._rid

    @property
    def weight(self):
        return self._weight

    @property
    def weight_lbs(self):
        return Respondent.kg_to_lb(self.weight)

    @property
    def height(self):
        return self._height

    @property
    def height_inches(self):
        return Respondent.cm_to_in(self.height)

    @property
    def age(self):
        return self._age

    @property
    def get_bmi(self):
        lb_weight = self.weight_lbs
        in_height = self.height_inches
        bmi = ((lb_weight / (in_height**2)) * 703)
        return bmi

    @property
    def gender_str(self):
        gender = int(self.gender)

        if gender == 1:
            return 'Male'
        else:
            return 'Female'

    @property
    def get_cpa(self):
        cpa = -110 + (1.34 * self.chest_di) + (1.54 * self.chest_depth) + (1.20 * self.bitrochanteric_di) + \
              (1.11 * self.wrist_gir) + (1.15 * self.ankle_gir) + (0.177 * self.height)
        return cpa

# -----------------------------------------------------------------------------------------#

    # list of "setters"

    @rid.setter
    def rid(self, new_rid):
        self._rid = new_rid

    @age.setter
    def age(self, new_age):
        self._age = new_age

    @height.setter
    def height(self, new_height):
        self._height = new_height

    @weight.setter
    def weight(self, new_weight):
        self._weight = new_weight

    @gender.setter
    def gender(self, new_gender):
        self._gender = new_gender

# -----------------------------------------------------------------------------------------#
    # basic methods for conversion

    @staticmethod
    def kg_to_lb(kg_weight):
        lb_weight = kg_weight * 2.20462
        return lb_weight

    @staticmethod
    def cm_to_in(cm_height):
        in_height = (cm_height * 0.393701)
        return in_height