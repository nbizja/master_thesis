class MarkovChain():

    def __init__(self, userList, accessPoints):
        self.userList = userList
        self.accessPoints = accessPoints

    def initializeChains(self):
        emptyChains = {}
        chain = {}
        for ap in self.accessPoints:
            chain[ap] = {a:0 for a in self.accessPoints}

        return {u:chain for u in self.userList}

    def computeMarkovChain(self, movementPattern):
        chains = self.initializeChains()

        previousStates = {}
        for mp in movementPattern:
            apPosition = mp['AP'].find('AP')
            buildingName = mp['AP'][0:apPosition]
            
            if int(mp['userId']) in previousStates:
                chains[int(mp['userId'])][previousStates[int(mp['userId'])]][buildingName] += 1

            previousStates[int(mp['userId'])] = buildingName


        for u in self.userList:
            for ap in chains[u].keys():
                totalRequests = sum(chains[u][ap].values())
                if totalRequests > 0:
                    for ap2 in chains[u][ap].keys():
                        chains[u][ap][ap2] /= float(totalRequests)


        return chains



if __name__ == '__main__':
    popBuildings = ['AcadBldg16', 'ResBldg71', 'ResBldg92', 'ResBldg20', 'ResBldg31', 'AcadBldg10', 'ResBldg55', 'AcadBldg34', 'ResBldg57', 'AcadBldg31', 'AcadBldg30', 'AcadBldg33', 'AcadBldg18', 'ResBldg36', 'ResBldg13', 'LibBldg3', 'ResBldg15', 'OthBldg4', 'ResBldg30', 'ResBldg60', 'AdmBldg20', 'ResBldg38', 'ResBldg3', 'ResBldg91', 'ResBldg90', 'ResBldg93', 'AcadBldg29', 'ResBldg74', 'ResBldg94', 'ResBldg97', 'AthlBldg3', 'AthlBldg11', 'AthlBldg10', 'LibBldg2', 'SocBldg11', 'ResBldg41', 'ResBldg44', 'LibBldg1', 'ResBldg66', 'AthlBldg8', 'ResBldg54', 'ResBldg62', 'ResBldg63', 'AcadBldg26', 'AthlBldg2', 'ResBldg22', 'ResBldg23', 'ResBldg25', 'ResBldg43', 'SocBldg1', 'SocBldg3', 'SocBldg4', 'ResBldg21', 'ResBldg69', 'ResBldg82', 'ResBldg83', 'ResBldg80', 'ResBldg101', 'ResBldg87', 'ResBldg84', 'AcadBldg6', 'ResBldg100', 'AcadBldg4', 'ResBldg33']
    popU = [2304, 3587, 4182, 3590, 1031, 2058, 4013, 4113, 18, 531, 3094, 4632, 4634, 4124, 4698, 1541, 32, 3504, 548, 550, 4135, 2147, 3625, 554, 2604, 2093, 558, 3848, 1074, 2611, 4660, 4149, 4150, 2616, 569, 574, 4671, 2113, 3138, 2230, 1094, 1608, 586, 589, 3153, 2643, 84, 3158, 4640, 600, 2867, 3674, 1627, 3164, 2653, 2655, 1906, 2747, 1126, 4711, 2665, 2154, 1127, 3379, 2669, 2671, 112, 2161, 1862, 3567, 4728, 1145, 1658, 3196, 4734, 2687, 4225, 1154, 1643, 132, 3719, 648, 1161, 3210, 1303, 3725, 1679, 1168, 4659, 3551, 1175, 3736, 3737, 51, 3229, 3230, 1184, 1697, 4263, 2728, 1308, 4266, 3757, 968, 4432, 694, 1720, 2745, 698, 4283, 1029, 2752, 2753, 3266, 195, 708, 2422, 710, 2760, 2761, 715, 3276, 3570, 1880, 3284, 1239, 2264, 4826, 4828, 2170, 3451, 4836, 2277, 298, 636, 2283, 2289, 1778, 467, 2804, 1269, 246, 2601, 3832, 4859, 4348, 1789, 767, 2816, 2347, 4872, 3853, 3854, 3343, 3859, 2838, 2839, 3864, 4740, 795, 796, 3034, 4382, 4485, 289, 1578, 292, 3877, 4902, 2858, 135, 818, 1839, 4402, 3123, 1357, 3895, 3386, 4923, 2954, 3902, 3055, 835, 3382, 326, 481, 1816, 1865, 331, 1356, 333, 335, 848, 1873, 3410, 2387, 2900, 2901, 4440, 2788, 4442, 3215, 860, 2874, 1253, 3216, 3427, 2534, 3943, 2921, 1386, 876, 2365, 4464, 3441, 4493, 830, 3446, 2937, 2426, 4475, 381, 998, 3985, 1921, 1515, 2436, 3461, 4486, 3463, 3977, 906, 578, 1934, 911, 4497, 3474, 3989, 3225, 922, 2459, 1948, 1949, 1497, 4003, 1956, 2630, 412, 754, 3502, 3741, 944, 4529, 1182, 841, 4340, 2185, 2492, 2498, 3011, 452, 3015, 4040, 3017, 4785, 1997, 4047, 2001, 2515, 2005, 4054, 4569, 986, 2895, 4636, 3039, 4064, 2529, 2530, 3835, 4581, 4070, 4177, 1000, 1788, 2915, 2027, 3389, 2031, 4592, 4081, 1522, 4595, 2548, 681, 505, 507, 1020, 4605, 3070]

    markovChain = MarkovChain(popU, popBuildings)

    fieldnames = ['timestamp', 'userId', 'AP']
    import csv

    with open('/data/clean_movement.csv', 'rb') as csvfile:
        movementPattern = csv.DictReader(csvfile, fieldnames, delimiter=',')
        chains = markovChain.computeMarkovChain(movementPattern)
    
    print chains
         
