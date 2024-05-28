        a2_number, a3_number, a4_number = 70, 100, 20
        dUnit, unit = '', ''
        # A1--------------------------
        A1_display()
        # for testing-----------
        if (dif//10) % 2 == 0:
            a1_number = 120 # for testing
        else:
            a1_number = 80
        # A1--------------------------

        # A2--------------------------
        # for testing-----------
        if a2_number < 120:
            a2_number = 70 + int(dif)%50
        else:
            a2_number = 70
        if (dif//10) % 3 == 0:
            A2_L_display() # for testing
        elif (dif//10) % 3 == 1:
            A2_R_display()
        else:
            A2_B_display()
        # for testing-----------
        # A2---------------------------
        
        # A3---------------------------
        # for testing-----------
        if dif < 10:
            pass
        elif dif < 20:
            A3_MH_display()
        elif dif < 30:
            A3_MS_display()
        elif dif < 40:
            A3_SF_display()
        elif dif < 50:
            A3_BL_display()
        elif dif < 60:
            A3_BF_display()
        if dif >= 10 and dif < 60:
            p = 1
        # for testing-----------
        # A3----------------------------

        # B5/B6-------------------------
        # for testing-----------
        if (dif//10) % 2 == 0:
            B5_display()
        else:
            B6_display() # for testing
        # for testing-----------
        # B5/B6-------------------------

        # B3----------------------------------
        # for testing------------------
        if dif < 10:
            pass
        elif dif< 15:
            B3_P_display(1)
        elif dif < 20:
            B3_P_display(2)
        elif dif < 25:
            B3_P_display(3)
        elif dif < 30:
            B3_P_display(4)
        elif dif < 35:
            B3_F_L1_display()
        elif dif < 40:
            B3_F_L2_display()
        elif dif < 45:
            B3_P_L1_display()
        elif dif < 50:
            B3_P_L2_display()
        if dif >= 10 and dif < 50:  
            p = 1
            a = 1
        # for testing------------------
        # B3----------------------------------

        # B4----------------------------------
        # for testing---------------
        if dif >= 50 and dif < 60:
            B4_L_display()
            p = 2
        elif dif >= 60 and dif < 70:
            B4_R_display()
            p = 2
        # for testing---------------
        # B4----------------------------------

        # A4 value----------------------------
        # for testing-------------
        if a3_number > 1:
            a3_number = 100 - 3*(int(dif)%33)
            a4_number = a3_number
            unit = 'm'
        elif a3_number >= 0:
            a3_number = -1
            a4_number = 0
            dUnit = 'm'
        else:
            a3_number = 100
            a4_number = a3_number
            unit = 'm'

        # for testing-------------
        # A4 value----------------------------

        # A4 pattern--------------------------
        # for testing-------------
        if dif < 70:
            pass
        elif dif < 80:
            if lastA4 != 'S':
                start = 0
            lastA4 = 'S'
            A4_S_display()
            if p == 3:
                B1_S_display()
        elif dif < 99:
            if lastA4 != 'TL':
                start = 0
            lastA4 = 'TL'
            A4_TL_display()
            if p == 3 and unit == 'm' and a3_number < 50 and start == 0:
                start = dif * 1000
                B1_L_Near_display(start)
            elif p == 3 and unit == 'm' and a3_number < 50:
                B1_L_Near_display(start)
            elif p == 3:
                B1_L_Far_display()
        elif dif < 132:
            if lastA4 != 'TR':
                start = 0
            lastA4 = 'TR'
            A4_TR_display()
            if p == 3 and unit == 'm' and a3_number < 50 and start == 0:
                start = dif * 1000
                B1_R_Near_display(start)
            elif p == 3 and unit == 'm' and a3_number < 50:
                B1_R_Near_display(start)
            elif p == 3:
                B1_R_Far_display()
        elif dif < 165:
            if lastA4 != 'TA':
                start = 0
            lastA4 = 'TA'
            A4_TA_display()
            if p == 3 and unit == 'm' and a3_number < 50 and start == 0:
                start = dif * 1000
                B1_A_Near_display(start)
            elif p == 3 and unit == 'm' and a3_number < 50:
                B1_A_Near_display(start)
            elif p == 3:
                B1_A_Far_display()
        # for testing-------------
        # A4 pattern--------------------------