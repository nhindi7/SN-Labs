from project_modules import * # this line imports all libraries or modules used for implementing the DVI

# A function that crops or removes out the white background of NEOM/OXAGON logos
def crop_white_background(image_path):
    # This statement opens the image file in a reading mode
    image = Image.open(image_path)
    # This converts an image file from RGBA format to black and white format
    image = image.convert("RGBA")
    # This retrieves the width and height of an image file
    width, height = image.size

    # This loop starts out the process of cropping out the white background of NEOM/OXAGON logos
    for y in range(height):
        for x in range(width):
            r, g, b, a = image.getpixel((x, y))
            if r == 255 and g == 255 and b == 255 and a == 255:
                image.putpixel((x, y), (255, 255, 255, 0))

    # This statement surrounds the box of the logo itself
    bbox = image.getbbox()
    # This crops the surrounded box of the logo
    cropped_image = image.crop(bbox)

    # returns the value of the cropped box
    return cropped_image

# A class of methods as functions that generate the outputs of demand models for different NEOM sectors
class project_collection:
    # A method that produces the output of Demand Model for the air mobility sector
    def airport_CAPEX_OPEX(self, base_input, currency_exchange, CPA_categories, FTE, CPA_reference, \
        selected_options, CPA_column_index, FTE_2, retail_cbm, main_tab, amtab):

        # An input for the revenue tenancy
        revenue_tenancy = base_input.iloc[0, :]
        # An input for the airport OPEX in SAR
        airport_OPEX_SAR = base_input.iloc[3, :]
        # An input for the airport revenue
        airport_revenue = base_input.iloc[1, :]
        # An empty list for proposed prices
        prop_price = []
        # An empty list for cbm to kg conversion factors
        cbm_kg = []
        # An empty list for volume in cbm per employee
        volume_employee = []
        # An empty list for the costs per volumes per CPAs
        moneyCBM_per_CPA = []
        # An empty list for the costs per employees per CPAs
        moneyEmployee_per_CPA = []
        # An empty list for the airport CAPEX
        airportCAPEX = []

        # An empty list for the OPEX tenants
        OPEX_tenants = []
        # This loop represents the process of appending the calculation of each OPEX tenant
        for row_index in range(8):
            OPEX_tenants.append(revenue_tenancy[row_index] * airport_OPEX_SAR[row_index] / airport_revenue[row_index])

        # An empty list for the whole budget of OPEX tenants
        OPEX_tenants_USD = []

        # This loop represents the process of appending the calculation of the whole budget of OPEX tenants
        for row_index in range(len(OPEX_tenants)):
            OPEX_tenants_USD.append(OPEX_tenants[row_index] * currency_exchange)

        # An empty list for the total OPEX
        total_OPEX = []

        # This loop represents the process of appending the calculation of total OPEX
        for row_index in range(len(OPEX_tenants)):
            total_OPEX.append(airport_OPEX_SAR[row_index] * currency_exchange + OPEX_tenants_USD[row_index])

        # An empty list for the tenancy factor
        tenancy_factor = []

        # This loop represents the process of appending the calculation of tenancy factor
        for row_index in range(len(total_OPEX)):
            tenancy_factor.append(total_OPEX[row_index] / sum(total_OPEX) * 0.35)

        # This loop represents the process of appending the vectors of proposed price, cbm to kg factors, and then volume per employee
        for c_index in range(len(CPA_categories.iloc[0, :])):
            for r_index in CPA_categories.iloc[1:, c_index]:
                if c_index == 0:
                    prop_price.append(r_index)
                elif c_index == 1:
                    cbm_kg.append(r_index)
                elif c_index == 3:
                    volume_employee.append(r_index)

        # This loop represents the process of appending the calculation of volume in CBM per CPA
        for i in range(len(CPA_categories.iloc[1:, 0])):
            moneyCBM_per_CPA.append(prop_price[i] * currency_exchange / cbm_kg[i])

        # This loop represents the process of appending the calculation of budget of employee per CPA
        for j in range(len(CPA_categories.iloc[1:, 0])):
            moneyEmployee_per_CPA.append(moneyCBM_per_CPA[j] * volume_employee[j])

        # An empty list of money percentages of employees
        percentage_money_employee = []

        # This loop represents the process of appending the calculation of money percentages of employees
        for money_index in range(len(moneyEmployee_per_CPA)):
            percentage_money_employee.append(moneyEmployee_per_CPA[money_index] / sum(moneyEmployee_per_CPA))

        # An empty list of airport CAPEX
        airportCapex = []

        # This loop represents the process of appending the calculation of airport CAPEX
        for k in range(len(FTE)):
            summed_value = 0
            for l in range(len(CPA_reference)):
                airportCapex.append(FTE[k]*moneyEmployee_per_CPA[l]/1000000)
                summed_value += FTE[k]*moneyEmployee_per_CPA[l]/1000000
            airportCAPEX.append(summed_value)
        
        # This is a Pandas data frame for the CPA index
        airportCAPEX_df_index = pd.DataFrame({'CPA Category':CPA_column_index})
        # This is a Pandas data frame for the Airport CAPEX
        airportCAPEX_df_res = pd.DataFrame({'2026': airportCapex})
        # This moves the next airport CAPEX values to the next column or year
        airportCAPEX_df_res['2027'] = airportCAPEX_df_res['2026'].iloc[92:184].reset_index(drop=True)
        # This moves the next airport CAPEX values to the next column or year
        airportCAPEX_df_res['2028'] = airportCAPEX_df_res['2026'].iloc[184:276].reset_index(drop=True)
        # This moves the next airport CAPEX values to the next column or year
        airportCAPEX_df_res['2029'] = airportCAPEX_df_res['2026'].iloc[276:368].reset_index(drop=True)
        # This moves the next airport CAPEX values to the next column or year
        airportCAPEX_df_res['2030'] = airportCAPEX_df_res['2026'].iloc[368:460].reset_index(drop=True)
        # This moves the next airport CAPEX values to the next column or year
        airportCAPEX_df_res['2031'] = airportCAPEX_df_res['2026'].iloc[460:552].reset_index(drop=True)
        # This moves the next airport CAPEX values to the next column or year
        airportCAPEX_df_res['2032'] = airportCAPEX_df_res['2026'].iloc[552:644].reset_index(drop=True)
        # This moves the next airport CAPEX values to the next column or year
        airportCAPEX_df_res['2033'] = airportCAPEX_df_res['2026'].iloc[644:736].reset_index(drop=True)
        # This moves the next airport CAPEX values to the next column or year
        airportCAPEX_df_res['2026'] = airportCAPEX_df_res['2026'].iloc[:-len(airportCapex)+92]
        # This concatenates the two Pandas data frames
        airportCAPEX_df = pd.concat([airportCAPEX_df_index, airportCAPEX_df_res], axis = 1)
        # This generates an Excel file for Airport CAPEX values
        airportCAPEX_df.to_excel("AirportCAPEX.xlsx", sheet_name = "CAPEX", index = False)
        
        # An empty list of recurring CAPEX values
        recurringCAPEX = []
        # An empty list of remaining CAPEX values
        remainingCAPEX = []
        # An empty list of recurring Airport CAPEX values
        recurringAirportCAPEX = []

        # This loop represents the process of appending the calculation of recurring CAPEX
        for recur_index in range(len(airportCapex)):
            recurringCAPEX.append(airportCapex[recur_index] * 0.025)

        # This loop represents the process of appending the calculation of remaining CAPEX
        for remaining_index in range(len(recurringCAPEX)):
            if sum(airportCapex) >= recurringCAPEX[remaining_index]:
                remainingCAPEX.append(recurringCAPEX[remaining_index])
            else:
                remainingCAPEX.append(recurringCAPEX[remaining_index] - sum(airportCapex))

        # This loop represents the process of appending the calculation of recurring Airport CAPEX
        for recur_CAPEX in range(len(remainingCAPEX)):
            recurringAirportCAPEX.append(remainingCAPEX[recur_CAPEX])

        # This is a Pandas data frame for the CPA index
        airportRecurringCAPEX_df_index = pd.DataFrame({'CPA Category':CPA_column_index})
        # This is a Pandas data frame for the recurring Airport CAPEX
        airportRecurringCAPEX_df_res = pd.DataFrame({'2026': recurringAirportCAPEX})
        # This moves the next airport CAPEX values to the next column or year
        airportRecurringCAPEX_df_res['2027'] = airportRecurringCAPEX_df_res['2026'].iloc[92:184].reset_index(drop=True)
        # This moves the next airport CAPEX values to the next column or year
        airportRecurringCAPEX_df_res['2028'] = airportRecurringCAPEX_df_res['2026'].iloc[184:276].reset_index(drop=True)
        # This moves the next airport CAPEX values to the next column or year
        airportRecurringCAPEX_df_res['2029'] = airportRecurringCAPEX_df_res['2026'].iloc[276:368].reset_index(drop=True)
        # This moves the next airport CAPEX values to the next column or year
        airportRecurringCAPEX_df_res['2030'] = airportRecurringCAPEX_df_res['2026'].iloc[368:460].reset_index(drop=True)
        # This moves the next airport CAPEX values to the next column or year
        airportRecurringCAPEX_df_res['2031'] = airportRecurringCAPEX_df_res['2026'].iloc[460:552].reset_index(drop=True)
        # This moves the next airport CAPEX values to the next column or year
        airportRecurringCAPEX_df_res['2032'] = airportRecurringCAPEX_df_res['2026'].iloc[552:644].reset_index(drop=True)
        # This moves the next airport CAPEX values to the next column or year
        airportRecurringCAPEX_df_res['2033'] = airportRecurringCAPEX_df_res['2026'].iloc[644:736].reset_index(drop=True)
        # This moves the next airport CAPEX values to the next column or year
        airportRecurringCAPEX_df_res['2026'] = airportRecurringCAPEX_df_res['2026'].iloc[:-len(recurringAirportCAPEX)+92]
        # This concatenates the two Pandas data frames
        airportRecurringCAPEX_df = pd.concat([airportRecurringCAPEX_df_index, airportRecurringCAPEX_df_res], axis = 1)
        # This generates an Excel file for recurring Airport CAPEX values
        airportRecurringCAPEX_df.to_excel("AirportRecurringCAPEX.xlsx", sheet_name = "RecurringCAPEX", index = False)

        # An empty list of Airport OPEX per CPA values 
        airportOPEX_perCPA = []
        # An empty list of Airport OPEX values 
        airportOPEX = []

        # This loop represents the process of appending the calculation of Airport OPEX
        for fte_index in range(len(FTE_2)):
            summed_value = 0
            for opex_index in range(len(CPA_reference)):
                airportOPEX.append((np.float64(moneyEmployee_per_CPA[opex_index]) * np.float64(FTE_2[fte_index])) / 1000000 + retail_cbm[opex_index][fte_index])
                summed_value += (np.float64(moneyEmployee_per_CPA[opex_index]) * np.float64(FTE_2[fte_index])) / 1000000 + retail_cbm[opex_index][fte_index]
            airportOPEX_perCPA.append(summed_value)

        # This is a Pandas data frame for the CPA index
        airportOPEX_df_index = pd.DataFrame({'CPA Category':CPA_column_index})
        # This is a Pandas data frame for the Airport OPEX
        airportOPEX_df_res = pd.DataFrame({'2026': airportOPEX})
        # This moves the next airport CAPEX values to the next column or year
        airportOPEX_df_res['2027'] = airportOPEX_df_res['2026'].iloc[92:184].reset_index(drop=True)
        # This moves the next airport CAPEX values to the next column or year
        airportOPEX_df_res['2028'] = airportOPEX_df_res['2026'].iloc[184:276].reset_index(drop=True)
        # This moves the next airport CAPEX values to the next column or year
        airportOPEX_df_res['2029'] = airportOPEX_df_res['2026'].iloc[276:368].reset_index(drop=True)
        # This moves the next airport CAPEX values to the next column or year
        airportOPEX_df_res['2030'] = airportOPEX_df_res['2026'].iloc[368:460].reset_index(drop=True)
        # This moves the next airport CAPEX values to the next column or year
        airportOPEX_df_res['2031'] = airportOPEX_df_res['2026'].iloc[460:552].reset_index(drop=True)
        # This moves the next airport CAPEX values to the next column or year
        airportOPEX_df_res['2032'] = airportOPEX_df_res['2026'].iloc[552:644].reset_index(drop=True)
        # This moves the next airport CAPEX values to the next column or year
        airportOPEX_df_res['2033'] = airportOPEX_df_res['2026'].iloc[644:736].reset_index(drop=True)
        # This moves the next airport CAPEX values to the next column or year
        airportOPEX_df_res['2026'] = airportOPEX_df_res['2026'].iloc[:-len(airportOPEX)+92]
        # This concatenates the two Pandas data frames
        airportOPEX_df = pd.concat([airportOPEX_df_index, airportOPEX_df_res], axis = 1)
        # This generates an Excel file for Airport OPEX values
        airportOPEX_df.to_excel("AirportOPEX.xlsx", sheet_name = "OPEX", index = False)

        # Create a Random Forest Regressor object
        airportCapexOpexMatrix = RandomForestRegressor()
        # Train the model
        airportCapexOpexMatrix.fit(np.reshape(airportCAPEX, (-1, 1)), np.reshape(airportOPEX_perCPA, (-1, 1)))
        # Predict on new data
        airportCapexPredictions = airportCapexOpexMatrix.predict(np.reshape(airportCAPEX, (-1, 1)))
        # Calculate R2 (Pearson Correlation Coefficient) value
        airport_CAPEXOPEX_R2 = r2_score(np.reshape(airportOPEX_perCPA, (-1, 1)), airportCapexPredictions)
        # Calculate the area under the curve of Random Forest Regression for Airport CAPEX & OPEX
        airport_CAPEXOPEX_area = integrate.simps(airportCapexPredictions, airportCAPEX)
        
        # This layout visualizes and forecasts the annual Airport CAPEX
        layout6 = html.Div([
            html.Div([
                dcc.Graph(id='bar-graph0',
                    figure = go.Figure(
                        data=[go.Bar(x=['2026', '2027', '2028', '2029', '2030', '2031', '2032', '2033'], y = airportCAPEX, marker={'color': 'blue'}, name='Value'),
                        go.Scatter(
                            x=['2026', '2027', '2028', '2029', '2030', '2031', '2032', '2033'],
                            y=[val/2 for val in airportCAPEX],
                            mode='lines+markers',
                            line={'color': 'red'},
                            marker={'symbol': 'circle','size': 10, 'color': 'orange'},
                            name='Moving Average')],
                        layout=go.Layout(title = 'Annual Demand Model Output of Airport CAPEX',
                                        title_x=0.5,
                                        xaxis=dict(title='Year'),
                                        yaxis=dict(title='Airport CAPEX (in million SAR)'))))
                ]),
            html.Iframe(
                id='map-graph',
                src="https://www.google.com/maps/embed/v1/place?key=AIzaSyA2kz9F_7Jw43snykMWvBjdiWySUgf0JmA&q=27.572418511924152,35.536511500684576",
                style={"width": "100%", "height": "600px"}
               )
            ])

        # This layout visualizes and forecasts the annual Airport OPEX
        layout7 = html.Div([
            html.Div([
                dcc.Graph(id='bar-graph8',
                    figure = go.Figure(
                        data=[go.Bar(x=['2025', '2026', '2027', '2028', '2029', '2030', '2031', '2032'], y = airportOPEX_perCPA, marker={'color': 'blue'}, name='Value'),
                        go.Scatter(
                            x=['2025', '2026', '2027', '2028', '2029', '2030', '2031', '2032'],
                            y=[val/2 for val in airportOPEX_perCPA],
                            mode='lines+markers',
                            line={'color': 'red'},
                            marker={'symbol': 'circle','size': 10, 'color': 'orange'},
                            name='Moving Average')],
                        layout=go.Layout(title = 'Annual Demand Model Output of Airport OPEX',
                                        title_x=0.5,
                                        xaxis=dict(title='Year'),
                                        yaxis=dict(title='Airport OPEX (in million SAR)'))))
                ]),
            html.Iframe(
                id='map-graph',
                src="https://www.google.com/maps/embed/v1/place?key=AIzaSyA2kz9F_7Jw43snykMWvBjdiWySUgf0JmA&q=27.572418511924152,35.536511500684576",
                style={"width": "100%", "height": "600px"}
               )
            ])
        
        # This layout visualizes the Random Forest Regression of both Airport CAPEX and OPEX
        layout9 = html.Div([
                html.Div([
                    dcc.Graph(
                        id='matplotlib-graph',
                        figure=go.Figure(
                            data=[
                                go.Scatter(x = airportCAPEX, y = airportCapexPredictions, mode = 'lines', name='Line of Best Fit', line={'color': 'blue'}, fill='tozeroy'),
                                go.Scatter(x = airportCAPEX, y = airportCapexPredictions, mode = 'markers', name = 'Predicted Value', 
                                            marker={'symbol': 'circle','size': 10, 'color': 'orange'}),
                                go.Scatter(x=np.concatenate([airportCAPEX, airportCAPEX[::-1]]), y=np.concatenate([airportCapexPredictions, np.zeros_like(airportCapexPredictions[::-1])]), fill='tozeroy', mode='none', name='Area Under Curve')
                                ],
                            layout = go.Layout(title = 'Scatter Plot of Predicted Values of CAPEX & OPEX',
                                                annotations=[
                                                    dict(
                                                        x=0.5,
                                                        y=1.1,
                                                        text=f'R^2: {airport_CAPEXOPEX_R2:.4f}, R: {math.sqrt(airport_CAPEXOPEX_R2):.4f}, CAPEX+OPEX: {airport_CAPEXOPEX_area:.2f}',
                                                        showarrow=False,
                                                        xref='paper',
                                                        yref='paper',
                                                        xanchor='center',
                                                        yanchor='bottom',
                                                        font=dict(size=14)
                                                        )],
                                                showlegend = True,
                                                title_x=0.5,
                                                xaxis=dict(title='Airport CAPEX (in million SAR)'),
                                                yaxis=dict(title='Airport OPEX (in million SAR)'))))
                        ])
                    ])

        # This if statement block indicates the conditions of producing the layouts in the DVI whenever the user navigates among tabs and subtabs
        if main_tab == 'tab-am' and 'airMobility' in selected_options:
            if amtab == 'tab-1':
                return html.Div(layout6)
            elif amtab == 'tab-2':
                return html.Div(layout7)
            elif amtab == 'tab-3':
                return html.Div(layout9)

    # A method that produces the output of Demand Model for the Food and Beverage sector
    def foodBeverage(self, all_tourist, all_resident, CPA_column_split_index, usd_per_cbm, hotel_spend, selected_options, CPA_column_index, main_tab):
        # An empty list of business travelers
        business_travelers = []
        # An empty list of day-trippers
        day_tripper = []
        # An empty list of e-residents
        eresidents = []
        # An empty list of experiential tourists
        experiential_tourists = []
        # An empty list of shopping tourists
        shopping_tourist = []

        # This loop appends all varying tourists from the Food and Beverage sector
        for tourist_cindex in range(len(all_tourist[0])):
            for tourist_rindex in range(len(all_tourist)):
                if tourist_rindex % 15 == 0 or tourist_rindex % 15 == 2 or tourist_rindex % 15 == 9:
                    business_travelers.append(all_tourist[tourist_rindex][tourist_cindex])
                elif tourist_rindex % 15 == 1 or tourist_rindex % 15 == 3 or tourist_rindex % 15 == 7 \
                    or tourist_rindex % 15 == 10 or tourist_rindex % 15 == 11 or tourist_rindex % 15 == 12 \
                    or tourist_rindex % 15 == 13 or tourist_rindex % 15 == 14:
                    experiential_tourists.append(all_tourist[tourist_rindex][tourist_cindex])
                elif tourist_rindex % 15 == 4:
                    day_tripper.append(all_tourist[tourist_rindex][tourist_cindex])
                elif tourist_rindex % 15 == 6:
                    eresidents.append(all_tourist[tourist_rindex][tourist_cindex])
                elif tourist_rindex % 15 == 7 or tourist_rindex % 15 == 8:
                    shopping_tourist.append(all_tourist[tourist_rindex][tourist_cindex])
        
        # This is the average annual income of business travelers
        business_traveler_income = 5685
        # This is the average annual income of e-residents
        eresident_income = 41720
        # This is the average annual income of day-trippers
        day_tripper_income = 997
        # This is the average annual income of shopping tourists
        shopping_tourist_income = 12600
        # This is the average annual income of experiential tourists
        experiential_tourist_income = 8574

        # This is the split ratio for business travelers
        business_traveler_split = 0.23
        # This is the split ratio for e-residents
        eresident_split = 0.23
        # This is the split ratio for day trippers
        day_tripper_split = 0.14
        # This is the split ratio for shopping tourists
        shopping_tourist_split = 0.07
        # This is the split ratio for experiential tourists
        experiential_tourist_split = 0.22

        # An empty list of annual tourist incomes
        annual_tourist_income = []

        # This loop appends the calculation of business travelers' incomes
        for c_index in range(len(business_travelers)):
            Bvalue = business_travelers[c_index] * business_traveler_split * business_traveler_income
            annual_tourist_income.append(Bvalue)
        
        # This loop appends the calculation of day-trippers' incomes
        for c_index in range(len(day_tripper)):
            Dvalue = day_tripper[c_index] * day_tripper_split * day_tripper_income
            annual_tourist_income.append(Dvalue)
        
        # This loop appends the calculation of e-residents' incomes
        for c_index in range(len(eresidents)):
            Evalue = eresidents[c_index] * eresident_split * eresident_income
            annual_tourist_income.append(Evalue)
        
        # This loop appends the calculation of experiential tourists' incomes
        for c_index in range(len(experiential_tourists)):
            EXvalue = experiential_tourists[c_index] * experiential_tourist_split * experiential_tourist_income
            annual_tourist_income.append(EXvalue)

        # This loop appends the calculation of shopping tourists' incomes
        for c_index in range(len(shopping_tourist)):
            Shvalue = shopping_tourist[c_index] * shopping_tourist_split * shopping_tourist_income
            annual_tourist_income.append(Shvalue)

        # An empty list of high-income residents 
        resident_high = []
        # An empty list of middle-income residents 
        resident_middle = []
        # An empty list of low-income residents 
        resident_low = []
        
        # This is the average annual income of high-income residents 
        resident_high_income = 838905
        # This is the average annual income of middle-income residents 
        resident_middle_income = 272195
        # This is the average annual income of low-income residents 
        resident_low_income = 69700

        # This is the split ratio for high-income residents 
        resident_high_income_split = 0.06
        # This is the split ratio for middle-income residents 
        resident_middle_income_split = 0.05
        # This is the split ratio for low-income residents 
        resident_low_income_split = 0.03

        # An empty list of all-income residents 
        annual_resident_income = []

        # This loop appends all varying residents from the Food and Beverage sector
        for resident_cindex in range(len(all_resident[0])):
            for resident_rindex in range(len(all_resident)):
                if resident_rindex % 3 == 0:
                    resident_high.append(all_resident[resident_rindex][resident_cindex])
                elif resident_rindex % 3 == 1:
                    resident_low.append(all_resident[resident_rindex][resident_cindex])
                elif resident_rindex % 3 == 2:
                    resident_middle.append(all_resident[resident_rindex][resident_cindex])

        # This loop appends the calculation of high-income residents' incomes
        for c_index in range(len(resident_high)):
            Hivalue = resident_high[c_index] * resident_high_income_split * resident_high_income
            annual_resident_income.append(Hivalue)

        # This loop appends the calculation of middle-income residents' incomes
        for c_index in range(len(resident_middle)):
            Lovalue = resident_middle[c_index] * resident_middle_income_split * resident_middle_income
            annual_resident_income.append(Lovalue)
        
        # This loop appends the calculation of low-income residents' incomes
        for c_index in range(len(resident_low)):
            Midvalue = resident_low[c_index] * resident_low_income_split * resident_low_income
            annual_resident_income.append(Midvalue)
        
        # This reshapes the list of annual tourists' incomes to Numpy 2D Arrays
        tourist_income_dims = (-1, 10)
        annual_tourist_income_new = np.reshape(annual_tourist_income, tourist_income_dims)

        # This reshapes the list of annual residents' incomes to Numpy 2D Arrays
        resident_income_dims = (-1, 10)
        annual_resident_income_new = np.reshape(annual_resident_income, resident_income_dims)

        # This concatenates the two Numpy 2D Arrays of both annual tourists' incomes and annual residents' incomes
        # by stacking them by row-wise
        fb_opex_Musd = np.row_stack((annual_resident_income_new, annual_tourist_income_new))

        # An empty list of F&B Total Spending OPEX values
        fb_total_spending_OPEX = []

        # This loop appends the calculation of F&B Total Spending OPEX values
        for c_index in range(len(fb_opex_Musd[0])):
            for r_index in range(len(fb_opex_Musd)):
                fb_total_spending_OPEX.append(fb_opex_Musd[r_index][c_index] * 0.8 / 1000000 * 0.27)

        # This reshapes the list of F&B Total Spending OPEX values to Numpy 2D Arrays
        fb_total_spending_OPEX_new = np.reshape(fb_total_spending_OPEX, (-1, 10))

        # This sums up the list of F&B Total Spending OPEX values with Numpy built-in function of sum
        fb_total_annual_sum = np.sum(fb_total_spending_OPEX_new, axis = 0)

        # An empty list of F&B Total Spending
        fb_total_spending_new = []

        # Another empty list of F&B Total Spending
        fb_total_spending_list = []

        # An empty list of F&B Total Spending Volumes in CBM
        fb_total_volume_list = []

        # An empty list of Annual Sums of F&B Total Spending Volumes in CBM
        fb_total_volume_list_sum = []

        # This entire loop shows the computation of F&B Total Spending Values in USD
        sum_summed_value = 0
        for hotel_cindex in range(len(fb_total_annual_sum)):
            for cpa_rindex in range(len(CPA_column_split_index)):
                if fb_total_annual_sum[hotel_cindex] * CPA_column_split_index[cpa_rindex] - hotel_spend[cpa_rindex][hotel_cindex] < 0:
                    resultant = fb_total_annual_sum[hotel_cindex] * CPA_column_split_index[cpa_rindex]
                    sum_summed_value += resultant
                    fb_total_spending_list.append(sum_summed_value)
                else:
                    resultant = fb_total_annual_sum[hotel_cindex] * CPA_column_split_index[cpa_rindex] - hotel_spend[cpa_rindex][hotel_cindex]
                    sum_summed_value += resultant
                    fb_total_spending_list.append(sum_summed_value)
            fb_total_spending_new.append(sum_summed_value)

        # This reshapes the list of F&B Total Spending OPEX values to Numpy 2D Arrays
        fb_total_spending_list_new = np.reshape(fb_total_spending_list, (92, 10))

        # This entire loop shows the computation of F&B Total Spending Volumes in CBM
        sum_summed_volume = 0
        for fb_cindex in range(len(fb_total_annual_sum)):
            for fb_rindex in range(len(CPA_column_split_index)):
                fb_total_volume_list.append(fb_total_spending_list_new[fb_rindex][fb_cindex] * 1e6 / usd_per_cbm[fb_rindex])
                sum_summed_volume += fb_total_spending_list_new[fb_rindex][fb_cindex] * 1e6 / usd_per_cbm[fb_rindex]
            fb_total_volume_list_sum.append(sum_summed_volume)

        # This is a Pandas data frame for the CPA index
        CPA_Category_Group_index = pd.DataFrame({'CPA Category': CPA_column_index})
        # This is a Pandas data frame for the list of F&B Total Incomes in USD
        fbOPEX_res = pd.DataFrame({'2021': fb_total_spending_list})
        # This moves the next airport CAPEX values to the next column or year
        fbOPEX_res['2022'] = fbOPEX_res['2021'].iloc[92:184].reset_index(drop=True)
        # This moves the next airport CAPEX values to the next column or year
        fbOPEX_res['2023'] = fbOPEX_res['2021'].iloc[184:276].reset_index(drop=True)
        # This moves the next airport CAPEX values to the next column or year
        fbOPEX_res['2024'] = fbOPEX_res['2021'].iloc[276:368].reset_index(drop=True)
        # This moves the next airport CAPEX values to the next column or year
        fbOPEX_res['2025'] = fbOPEX_res['2021'].iloc[368:460].reset_index(drop=True)
        # This moves the next airport CAPEX values to the next column or year
        fbOPEX_res['2026'] = fbOPEX_res['2021'].iloc[460:552].reset_index(drop=True)
        # This moves the next airport CAPEX values to the next column or year
        fbOPEX_res['2027'] = fbOPEX_res['2021'].iloc[552:644].reset_index(drop=True)
        # This moves the next airport CAPEX values to the next column or year
        fbOPEX_res['2028'] = fbOPEX_res['2021'].iloc[644:736].reset_index(drop=True)
        # This moves the next airport CAPEX values to the next column or year
        fbOPEX_res['2029'] = fbOPEX_res['2021'].iloc[736:828].reset_index(drop=True)
        # This moves the next airport CAPEX values to the next column or year
        fbOPEX_res['2030'] = fbOPEX_res['2021'].iloc[828:920].reset_index(drop=True)
        # This moves the next airport CAPEX values to the next column or year
        fbOPEX_res['2021'] = fbOPEX_res['2021'].iloc[:-len(fb_total_spending_list) + 92].reset_index(drop=True)
        # This concatenates the two Pandas data frames
        fb_opex_df = pd.concat([CPA_Category_Group_index, fbOPEX_res], axis = 1)
        # This generates an Excel file for F&B OPEX values
        fb_opex_df.to_excel("F&BOPEX.xlsx", sheet_name = "F&BOPEX", index = False)

        # This is a Pandas data frame for the list of F&B Total Volumes in CBM
        fb_res = pd.DataFrame({'2021': fb_total_volume_list})
        # This moves the next airport CAPEX values to the next column or year
        fb_res['2022'] = fb_res['2021'].iloc[92:184].reset_index(drop=True)
        # This moves the next airport CAPEX values to the next column or year
        fb_res['2023'] = fb_res['2021'].iloc[184:276].reset_index(drop=True)
        # This moves the next airport CAPEX values to the next column or year
        fb_res['2024'] = fb_res['2021'].iloc[276:368].reset_index(drop=True)
        # This moves the next airport CAPEX values to the next column or year
        fb_res['2025'] = fb_res['2021'].iloc[368:460].reset_index(drop=True)
        # This moves the next airport CAPEX values to the next column or year
        fb_res['2026'] = fb_res['2021'].iloc[460:552].reset_index(drop=True)
        # This moves the next airport CAPEX values to the next column or year
        fb_res['2027'] = fb_res['2021'].iloc[552:644].reset_index(drop=True)
        # This moves the next airport CAPEX values to the next column or year
        fb_res['2028'] = fb_res['2021'].iloc[644:736].reset_index(drop=True)
        # This moves the next airport CAPEX values to the next column or year
        fb_res['2029'] = fb_res['2021'].iloc[736:828].reset_index(drop=True)
        # This moves the next airport CAPEX values to the next column or year
        fb_res['2030'] = fb_res['2021'].iloc[828:920].reset_index(drop=True)
        # This moves the next airport CAPEX values to the next column or year
        fb_res['2021'] = fb_res['2021'].iloc[:-len(fb_total_volume_list) + 92].reset_index(drop=True)
        # This concatenates the two Pandas data frames
        fb_df = pd.concat([CPA_Category_Group_index, fb_res], axis = 1)
        # This generates an Excel file for F&B OPEX volumes
        fb_df.to_excel("F&BOPEX_volume.xlsx", sheet_name = "F&BOPEXCBM", index = False)
        
        # This layout visualizes and forecasts the annual F&B OPEX values and volumes
        layout4 = html.Div([
            html.Div([
                dcc.Graph(id='bar-graph13',
                    figure = go.Figure(
                        data=[go.Bar(x=['2021', '2022', '2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030'], y = fb_total_spending_new, marker={'color': 'blue'}, name = 'Value'),
                            go.Scatter(
                                x=['2021', '2022', '2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030'],
                                y=[val/2 for val in fb_total_spending_new],
                                mode='lines+markers',
                                line={'color': 'red'},
                                marker={'symbol': 'circle','size': 10, 'color': 'orange'},
                                name='Moving Average')],
                        layout=go.Layout(title = 'Annual Demand Model Output of F&B',
                                        title_x=0.5,
                                        xaxis=dict(title='Year'),
                                        yaxis=dict(title='F&B (in million USD)'))))
                ]),
            html.Div([
                dcc.Graph(id='bar-graph33',
                    figure = go.Figure(
                        data=[go.Bar(x=['2021', '2022', '2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030'], y = fb_total_volume_list_sum, marker={'color': 'blue'}, name = 'Value'),
                            go.Scatter(
                                x=['2021', '2022', '2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030'],
                                y=[val/2 for val in fb_total_volume_list_sum],
                                mode='lines+markers',
                                line={'color': 'red'},
                                marker={'symbol': 'circle','size': 10, 'color': 'orange'},
                                name='Moving Average')],
                        layout=go.Layout(title = 'Annual Demand Model Output of F&B',
                                        title_x=0.5,
                                        xaxis=dict(title='Year'),
                                        yaxis=dict(title='F&B (in CBM)'))))
                ]),
            html.Iframe(
                id='map-graph',
                src="https://www.google.com/maps/embed/v1/place?key=AIzaSyA2kz9F_7Jw43snykMWvBjdiWySUgf0JmA&q=27.572418511924152,35.536511500684576",
                style={"width": "100%", "height": "600px"}
               )
            ])
            
        # This if statement block indicates the conditions of producing the layouts in the DVI whenever the user navigates among tabs and subtabs
        if main_tab == 'tab-fb' and 'FB' in selected_options:
            return html.Div(layout4)

    # A method that produces the output of Demand Model for the hospitality sector
    def hospitality_function(self, opex_to_region, uk_population, uk_opex, GBPtoUSD, hospitality_OPEX, usd_per_cbm_hosp, selected_options, CPA_column_index, main_tab):

        # This loop appends the calculation of Hospitality OPEX
        group_sum = 0
        for values in opex_to_region:
            for index in values:
                group_sum = index / uk_population * uk_opex * GBPtoUSD / 1000000
                hospitality_OPEX.append(group_sum)

        # This reshapes the list of Hospitality OPEX values to Numpy 2D Arrays
        hospitality_OPEX_new = np.reshape(hospitality_OPEX, (1296, 8))
        # An empty list of Hospitality OPEX values
        hospitality_OPEX_4 = []
        # An empty list of Hospitality OPEX volumes
        hospitality_OPEX_newSum = []

        # This loop appends the summation of Hospitality OPEX values
        for col in range(len(hospitality_OPEX_new[0])):
            sum_regions = 0
            for row in range(len(hospitality_OPEX_new)): 
                sum_regions += hospitality_OPEX_new[row][col]
            hospitality_OPEX_4.append(sum_regions)

        # This loop appends the calculation of Hospitality OPEX volumes
        for col in range(len(hospitality_OPEX_new[0])):
            sum_regions = 0
            for row in range(len(usd_per_cbm_hosp)): 
                sum_regions += hospitality_OPEX_new[row][col] * 1e6 / usd_per_cbm_hosp[row]
                hospitality_OPEX_newSum.append(sum_regions)

        # This is a Pandas data frame for the CPA index
        CPA_Category_Group_index = pd.DataFrame({'CPA Category':CPA_column_index})
        # This is a Pandas data frame for the list of Hospitality OPEX values
        hospitality_res = pd.DataFrame({'2023': hospitality_OPEX_4})
        # This moves the next airport CAPEX values to the next column or year
        hospitality_res['2024'] = hospitality_res['2023'].iloc[93:186].reset_index(drop=True)
        # This moves the next airport CAPEX values to the next column or year
        hospitality_res['2025'] = hospitality_res['2023'].iloc[186:279].reset_index(drop=True)
        # This moves the next airport CAPEX values to the next column or year
        hospitality_res['2026'] = hospitality_res['2023'].iloc[279:372].reset_index(drop=True)
        # This moves the next airport CAPEX values to the next column or year
        hospitality_res['2027'] = hospitality_res['2023'].iloc[372:465].reset_index(drop=True)
        # This moves the next airport CAPEX values to the next column or year
        hospitality_res['2028'] = hospitality_res['2023'].iloc[465:558].reset_index(drop=True)
        # This moves the next airport CAPEX values to the next column or year
        hospitality_res['2029'] = hospitality_res['2023'].iloc[558:651].reset_index(drop=True)
        # This moves the next airport CAPEX values to the next column or year
        hospitality_res['2030'] = hospitality_res['2023'].iloc[651:744].reset_index(drop=True)
        # This moves the next airport CAPEX values to the next column or year
        hospitality_res['2023'] = hospitality_res['2023'].iloc[:-len(hospitality_OPEX_4) + 93].reset_index(drop=True)
        # This concatenates the two Pandas data frames
        hospitality_df = pd.concat([CPA_Category_Group_index, hospitality_res], axis = 1)
        # This generates an Excel file for Hospitality OPEX values
        hospitality_df.to_excel("hospitality.xlsx", sheet_name = "HOSPITALITY", index = False)

        # This is a Pandas data frame for the list of Hospitality OPEX volumes
        hospitality_res_2 = pd.DataFrame({'2023': hospitality_OPEX_newSum})
        # This moves the next airport CAPEX values to the next column or year
        hospitality_res_2['2024'] = hospitality_res_2['2023'].iloc[93:186].reset_index(drop=True)
        # This moves the next airport CAPEX values to the next column or year
        hospitality_res_2['2025'] = hospitality_res_2['2023'].iloc[186:279].reset_index(drop=True)
        # This moves the next airport CAPEX values to the next column or year
        hospitality_res_2['2026'] = hospitality_res_2['2023'].iloc[279:372].reset_index(drop=True)
        # This moves the next airport CAPEX values to the next column or year
        hospitality_res_2['2027'] = hospitality_res_2['2023'].iloc[372:465].reset_index(drop=True)
        # This moves the next airport CAPEX values to the next column or year
        hospitality_res_2['2028'] = hospitality_res_2['2023'].iloc[465:558].reset_index(drop=True)
        # This moves the next airport CAPEX values to the next column or year
        hospitality_res_2['2029'] = hospitality_res_2['2023'].iloc[558:651].reset_index(drop=True)
        # This moves the next airport CAPEX values to the next column or year
        hospitality_res_2['2030'] = hospitality_res_2['2023'].iloc[651:744].reset_index(drop=True)
        # This moves the next airport CAPEX values to the next column or year
        hospitality_res_2['2023'] = hospitality_res_2['2023'].iloc[:-len(hospitality_OPEX_newSum) + 93].reset_index(drop=True)
        # This concatenates the two Pandas data frames
        hospitality_df_2 = pd.concat([CPA_Category_Group_index, hospitality_res_2], axis = 1)
        # This generates an Excel file for Hospitality OPEX summing values
        hospitality_df_2.to_excel("hospitality_new.xlsx", sheet_name = "HOSPITALITY2", index = False)
        
        # This layout visualizes and forecasts the annual Hospitality OPEX values and volumes
        layout5 = html.Div([
            html.Div([
                dcc.Graph(id='bar-graph21',
                    figure = go.Figure(
                        data=[go.Bar(x=['2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030'], y = hospitality_OPEX_4, marker={'color': 'blue'}, name = 'Value'),
                            go.Scatter(
                                x=['2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030'],
                                y=[val/2 for val in hospitality_OPEX_4],
                                mode='lines+markers',
                                line={'color': 'red'},
                                marker={'symbol': 'circle','size': 10, 'color': 'orange'},
                                name='Moving Average')],
                        layout=go.Layout(title = 'Demand Model Output of Hospitality OPEX',
                                        title_x=0.5,
                                        xaxis=dict(title='Year'),
                                        yaxis=dict(title='Hospitality OPEX (in million USD)'))))
                ]),
            html.Div([
                dcc.Graph(id='bar-graph41',
                    figure = go.Figure(
                        data=[go.Bar(x=['2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030'], y = hospitality_OPEX_newSum, marker={'color': 'blue'}, name = 'Value'),
                            go.Scatter(
                                x=['2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030'],
                                y=[val/2 for val in hospitality_OPEX_newSum],
                                mode='lines+markers',
                                line={'color': 'red'},
                                marker={'symbol': 'circle','size': 10, 'color': 'orange'},
                                name='Moving Average')],
                        layout=go.Layout(title = 'Demand Model Output of Hospitality OPEX',
                                        title_x=0.5,
                                        xaxis=dict(title='Year'),
                                        yaxis=dict(title='Hospitality OPEX (in CBM)'))))
                ]),
            html.Iframe(
                id='map-graph',
                src="https://www.google.com/maps/embed/v1/place?key=AIzaSyA2kz9F_7Jw43snykMWvBjdiWySUgf0JmA&q=27.572418511924152,35.536511500684576",
                style={"width": "100%", "height": "600px"}
               )
            ])
            
        # This if statement block indicates the conditions of producing the layouts in the DVI whenever the user navigates among tabs and subtabs
        if main_tab == 'tab-h' and 'Hospitality' in selected_options:
            return html.Div(layout5)

    # A method that produces the output of Demand Model for the Energy: Solar Energy Production sector
    def solar_energy_production(self, installed_capacity, panel_capacity, panel_volume, solar_panels_volume, selected_options, main_tab, energytab):

        # This loop appends the calculation of total volume of solar energy
        for panel_index in range(len(installed_capacity)):
            if panel_index > 0:
                total_volume_result = abs(installed_capacity[panel_index] - installed_capacity[panel_index - 1]) * 1e9 / panel_capacity * panel_volume
                solar_panels_volume.append(total_volume_result)
           
        # This is a Pandas data frame for the Year
        year_index = pd.DataFrame({'Year': ['2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030', '2031']})
        # This is a Pandas data frame for the list of Solar Panels' volumes
        solar_res = pd.DataFrame({'Volume': solar_panels_volume})
        # This concatenates the two Pandas data frames
        solar_df = pd.concat([year_index, solar_res], axis = 1)
        # This generates an Excel file for Solar Energy Volumes
        solar_df.to_excel("solar.xlsx", sheet_name = "SOLAR", index = False)

        # This layout visualizes and forecasts the annual Solar Energy values and volumes
        layout11 = html.Div([
                html.Div([
                    dcc.Graph(id='bar-graph22',
                        figure = go.Figure(
                            data=[go.Scatter(
                                    x=['2022', '2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030', '2031'],
                                    y=solar_panels_volume,
                                    mode='markers',
                                    marker={'symbol': 'circle','size': 10, 'color': 'blue'},
                                    name='Moving Average')],
                            layout=go.Layout(title = 'Demand Model Output of Solar Panel Volume',
                                            title_x=0.5,
                                            xaxis=dict(title='Year'),
                                            yaxis=dict(title='Solar Panel Volume (in CBM)'))))
                    ]),
                html.Iframe(
                    id='map-graph',
                    src="https://www.google.com/maps/embed/v1/place?key=AIzaSyA2kz9F_7Jw43snykMWvBjdiWySUgf0JmA&q=27.572418511924152,35.536511500684576",
                    style={"width": "100%", "height": "600px"}
                    )
            ])
            
        # This if statement block indicates the conditions of producing the layouts in the DVI whenever the user navigates among tabs and subtabs
        if main_tab == 'tab-e' and energytab == 'tab-10' and 'energySEPP' in selected_options:
            return html.Div(layout11)

    # A method that produces the output of Demand Model for the Energy: Hydrogen Facility sector
    def hydrogen_facility_function(self, hydrogen_capacity, *hydrogen_base_input, selected_options, number_of_employees, volume_per_employee_cbm, volume_per_employee_usd, main_tab, energytab):

        # This appends the base input of Hydrogen Capacity from the Excel template
        hydrogen_capacity.append(hydrogen_base_input[0])
        hydrogen_capacity.append(hydrogen_base_input[1])
        hydrogen_capacity.append(hydrogen_base_input[2])

        # This appends the base input of number of employees from the Excel template
        number_of_employees.append(hydrogen_base_input[3])
        number_of_employees.append(hydrogen_base_input[4])
        number_of_employees.append(hydrogen_base_input[5])

        # An empty list of each volume per employee per CPA
        volume_per_employee_per_cpa = []
        
        # This loop appends the calculation of total volume per employee per CPA for Hydrogen Facility
        for hydrogen_index in range(len(number_of_employees)):
            volume_result = []
            for product_index in range(len(volume_per_employee_usd)):
                volume_result.append(hydrogen_capacity[hydrogen_index] * volume_per_employee_usd[product_index] + \
                    number_of_employees[hydrogen_index] * volume_per_employee_cbm[product_index])
            volume_per_employee_per_cpa.append(sum(volume_result))
            
        # This is a Pandas data frame for the Year
        year_index = pd.DataFrame({'Year': ['2028', '2029', '2030']})
        # This is a Pandas data frame for the list of volume per employee per CPA for Hydrogen Facility
        hydrogen_facility_res = pd.DataFrame({'Volume': volume_per_employee_per_cpa})
        # This concatenates the two Pandas data frames
        hydrogen_facility_df = pd.concat([year_index, hydrogen_facility_res], axis = 1)
        # This generates an Excel file for Hydrogen Facility Volumes
        hydrogen_facility_df.to_excel("hydrogen_facility.xlsx", sheet_name = "HYDROGEN", index = False)

        # This layout visualizes and forecasts the annual Hydrogen Facility values and volumes
        layout12 = html.Div([
                html.Div([
                    dcc.Graph(id='bar-graph230',
                        figure = go.Figure(
                            data=[go.Bar(x=['2028', '2029', '2030'], y = volume_per_employee_per_cpa, marker={'color': 'blue'}, name = 'Value'),
                                go.Scatter(
                                    x=['2028', '2029', '2030'],
                                    y=[val/2 for val in volume_per_employee_per_cpa],
                                    mode='lines+markers',
                                    line={'color': 'red'},
                                    marker={'symbol': 'circle','size': 10, 'color': 'orange'},
                                    name='Moving Average')],
                            layout=go.Layout(title = 'Demand Model Output of Hydrogen Facility',
                                            title_x=0.5,
                                            xaxis=dict(title='Year'),
                                            yaxis=dict(title='Volume per Employee per CPA (in CBM)'))))
                    ]),
                html.Iframe(
                    id='map-graph',
                    src="https://www.google.com/maps/embed/v1/place?key=AIzaSyA2kz9F_7Jw43snykMWvBjdiWySUgf0JmA&q=27.572418511924152,35.536511500684576",
                    style={"width": "100%", "height": "600px"}
                    )
                ])
            
        # This if statement block indicates the conditions of producing the layouts in the DVI whenever the user navigates among tabs and subtabs
        if main_tab == 'tab-e' and energytab == 'tab-20' and 'energyHF' in selected_options:
            return html.Div(layout12)

    # A method that produces the output of Demand Model for the Energy: Electrolyzer sector
    def electrolyzer_function(self, hydrogen_electrolyzer_units, number_of_electrolyzers, revenue_oxagon, revenue_line, hydrogen_electrolyzer_cells, number_of_cells, \
        total_electrolyzer_capacity, electrolyzer_capacity, number_of_hydrogen_electrolyzers, output_of_electrolyzer_units, selected_options, summary_output_volume_oxagon, summary_output_volume_line, \
        main_tab, energytab):

        # This loop appends the calculation of Hydrogen Electrolyzer Units
        for electrolyzer_index in range(3):
            hydrogen_electrolyzer_units.append(number_of_electrolyzers[electrolyzer_index] / revenue_oxagon[electrolyzer_index] * revenue_line[electrolyzer_index] \
                + number_of_electrolyzers[electrolyzer_index])

        # This loop appends the calculation of Hydrogen Electrolyzer Cells
        for hydrogen_cell_index in range(3):
            hydrogen_electrolyzer_cells.append(number_of_cells[hydrogen_cell_index] / number_of_electrolyzers[hydrogen_cell_index] * \
                number_of_electrolyzers[hydrogen_cell_index] / revenue_oxagon[hydrogen_cell_index] * revenue_line[hydrogen_cell_index] + \
                number_of_cells[hydrogen_cell_index])

        # This loop appends the calculation of Total Electrolyzer Capacity
        for capacity_index in range(3):
            total_electrolyzer_capacity.append(number_of_electrolyzers[capacity_index] / revenue_oxagon[capacity_index] * revenue_line[capacity_index] \
                * 20 / 1000 + electrolyzer_capacity[capacity_index])

        # This loop appends the calculation of Total Output Volume within OXAGON
        for oxagon_electrolyzer_index in range(len(number_of_hydrogen_electrolyzers)):
            output_volume_oxagon_result = []
            for oxagon_volume_index in range(len(output_of_electrolyzer_units)):
                output_volume_oxagon_result.append(number_of_hydrogen_electrolyzers[oxagon_electrolyzer_index] * output_of_electrolyzer_units[oxagon_volume_index])
            summary_output_volume_oxagon.append(sum(output_volume_oxagon_result))

        # This loop appends the calculation of Total Output Volume within THE LINE
        for line_electrolyzer_index in range(len(number_of_hydrogen_electrolyzers)):
            output_volume_line_result = 0
            for line_volume_index in range(len(output_of_electrolyzer_units)):
                output_volume_line_result += (number_of_electrolyzers[line_electrolyzer_index] / revenue_oxagon[line_electrolyzer_index] * revenue_line[line_electrolyzer_index] * \
                    output_of_electrolyzer_units[line_volume_index])
            summary_output_volume_line.append(output_volume_line_result)

        # This is a Pandas data frame for the Year
        year_index = pd.DataFrame({'Year': ['2028', '2029', '2030']})
        # This is a Pandas data frame for the list of Total Output Volume within OXAGON
        output_volume_oxagon_res = pd.DataFrame({'Volume': summary_output_volume_oxagon})
        # This concatenates the two Pandas data frames
        output_volume_oxagon_df = pd.concat([year_index, output_volume_oxagon_res], axis = 1)
        # This generates an Excel file for Total Output Volume within OXAGON
        output_volume_oxagon_df.to_excel("Oxagon_volume.xlsx", sheet_name = "OXAGON Volume", index = False)

        # This is a Pandas data frame for the Year
        year_index = pd.DataFrame({'Year': ['2028', '2029', '2030']})
        # This is a Pandas data frame for the list of Total Output Volume within THE LINE
        output_volume_line_res = pd.DataFrame({'Volume': summary_output_volume_line})
        # This concatenates the two Pandas data frames
        output_volume_line_df = pd.concat([year_index, output_volume_line_res], axis = 1)
        # This generates an Excel file for Total Output Volume within THE LINE
        output_volume_line_df.to_excel("LINE_volume.xlsx", sheet_name = "LINE Volume", index = False)

        # This layout visualizes and forecasts the Total Output Volume within OXAGON and THE LINE
        layout13 = html.Div([
                html.Div([
                    dcc.Graph(id='bar-graph240',
                        figure = go.Figure(
                            data=[go.Bar(x=['2028', '2029', '2030'], y = summary_output_volume_oxagon, marker={'color': 'blue'}, name = 'Value'),
                                go.Scatter(
                                    x=['2028', '2029', '2030'],
                                    y=[val/2 for val in summary_output_volume_oxagon],
                                    mode='lines+markers',
                                    line={'color': 'red'},
                                    marker={'symbol': 'circle','size': 10, 'color': 'orange'},
                                    name='Moving Average')],
                            layout=go.Layout(title = 'Demand Model Output of Electrolyzers',
                                            title_x=0.5,
                                            xaxis=dict(title='Year'),
                                            yaxis=dict(title='Output Volume of NIC (in CBM)'))))
                    ]),
                html.Div([
                    dcc.Graph(id='bar-graph240',
                        figure = go.Figure(
                            data=[go.Bar(x=['2028', '2029', '2030'], y = summary_output_volume_line, marker={'color': 'blue'}, name = 'Value'),
                                go.Scatter(
                                    x=['2028', '2029', '2030'],
                                    y=[val/2 for val in summary_output_volume_line],
                                    mode='lines+markers',
                                    line={'color': 'red'},
                                    marker={'symbol': 'circle','size': 10, 'color': 'orange'},
                                    name='Moving Average')],
                            layout=go.Layout(title = 'Demand Model Output of Electrolyzers',
                                            title_x=0.5,
                                            xaxis=dict(title='Year'),
                                            yaxis=dict(title='Output Volume of LINE (in CBM)'))))
                    ]),
                html.Iframe(
                    id='map-graph',
                    src="https://www.google.com/maps/embed/v1/place?key=AIzaSyA2kz9F_7Jw43snykMWvBjdiWySUgf0JmA&q=27.572418511924152,35.536511500684576",
                    style={"width": "100%", "height": "600px"}
                    )
                ])

        # This if statement block indicates the conditions of producing the layouts in the DVI whenever the user navigates among tabs and subtabs
        if main_tab == 'tab-e' and energytab == 'tab-30' and 'energyE' in selected_options: # and option6 == True:
            return html.Div(layout13)

    # A method that produces the output of Demand Model for the Energy: Energy Distribution
    def energy_distribution_function(self, energy_distribution_recurCapex_usd, total_percentage_recurring_capex, recurring_Capex_breakdown, energy_distribution_capex_usd, nonlabor_costs, \
        adjusted_power_grid, opex_per_cpa, energy_distribution_opex_sar, selected_options, main_tab, energytab):

        # This loop appends the calculation of recurring CAPEX breakdown
        for capex_index in range(len(energy_distribution_recurCapex_usd)):
            for percent_index in range(len(total_percentage_recurring_capex)):
                recurring_Capex_breakdown.append(energy_distribution_capex_usd[capex_index] / 1000000 * total_percentage_recurring_capex[percent_index])

        # This reshapes the list of recurring CAPEX breakdown to Numpy 2D Arrays
        recurring_Capex_breakdown_new = np.reshape(recurring_Capex_breakdown, (len(total_percentage_recurring_capex), len(energy_distribution_recurCapex_usd)))
    
        # This loop appends the calculation of OPEX per CPA
        for opex_index in range(len(nonlabor_costs)):
            for power_index in range(len(adjusted_power_grid)):
                opex_per_cpa.append(nonlabor_costs[opex_index] * adjusted_power_grid[power_index])

        # An empty list of CAPEX and OPEX Output Volumes
        CapexOpex_Output_Volume = []

        # This loop appends the calculation of CAPEX and OPEX Output Volumes
        for capexOpex_index in range(len(energy_distribution_opex_sar)):
            volume_sum_result = 0
            for cpa_index in range(len(adjusted_power_grid)):
                volume_sum_result += (energy_distribution_opex_sar[capexOpex_index] * 0.27 / 1000000 * adjusted_power_grid[cpa_index] + \
                    recurring_Capex_breakdown_new[cpa_index][capexOpex_index])
            CapexOpex_Output_Volume.append(volume_sum_result)

        # This is a Pandas data frame for the Year
        year_index = pd.DataFrame({'Year': ['2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030']})
        # This is a Pandas data frame for the list of CAPEX and OPEX Output Volumes
        CapexOpex_Output_Volume_res = pd.DataFrame({'Volume': CapexOpex_Output_Volume})
        # This concatenates the two Pandas data frames
        CapexOpex_Output_Volume_df = pd.concat([year_index, CapexOpex_Output_Volume_res], axis = 1)
        # This generates an Excel file for Energy Distribution
        CapexOpex_Output_Volume_df.to_excel("energy_distribution.xlsx", sheet_name = "Energy Distribution Volume", index = False)

        # This layout visualizes and forecasts the CAPEX and OPEX Output Volumes
        layout14 = html.Div([
                html.Div([
                    dcc.Graph(id='bar-graph240',
                        figure = go.Figure(
                            data=[go.Bar(x=['2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030'], y = CapexOpex_Output_Volume, marker={'color': 'blue'}, name = 'Value'),
                                go.Scatter(
                                    x=['2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030'],
                                    y=[val/2 for val in CapexOpex_Output_Volume],
                                    mode='lines+markers',
                                    line={'color': 'red'},
                                    marker={'symbol': 'circle','size': 10, 'color': 'orange'},
                                    name='Moving Average')],
                            layout=go.Layout(title = 'Demand Model Output of Energy Distribution',
                                            title_x=0.5,
                                            xaxis=dict(title='Year'),
                                            yaxis=dict(title='Output Volume (in USD)'))))
                    ]),
                html.Iframe(
                    id='map-graph',
                    src="https://www.google.com/maps/embed/v1/place?key=AIzaSyA2kz9F_7Jw43snykMWvBjdiWySUgf0JmA&q=27.572418511924152,35.536511500684576",
                    style={"width": "100%", "height": "600px"}
               )])

        # This if statement block indicates the conditions of producing the layouts in the DVI whenever the user navigates among tabs and subtabs
        if main_tab == 'tab-e' and energytab == 'tab-40' and 'energyED' in selected_options:
            return html.Div(layout14)

    # A method that produces the output of Demand Model for the Energy: Nonsolar Energy Production
    def nonsolar_energy_production_function(self, solar_input, solar_panels_units, panel_capacity, solar_volume, solar_panel_length, solar_panel_width, unit_of_conversion, \
        density_of_steel, wind_input, turbine_power, wind_panels_units, turbine_volume, wind_volume, battery_input, solar_system_power, battery_units, solar_system_volume, \
        battery_volume, robot_volume, array_of_robots, robot_height, robot_width, robot_length, selected_options, main_tab, energytab):

        # This loop appends the calculation of Solar Panels' Units
        for panel_index in range(len(solar_input)):
            if panel_index > 0:
                solar_volume_result = abs(solar_input[panel_index] - solar_input[panel_index - 1]) * 1e9 / panel_capacity
                solar_panels_units.append(solar_volume_result)

        # This loop appends the calculation of Solar Volume
        for volume_index in range(len(solar_panels_units)):
            solar_volume.append(solar_panels_units[volume_index] * solar_panel_length * solar_panel_width * unit_of_conversion / density_of_steel)

        # This loop appends the calculation of Wind Panels' Units
        for wind_index in range(len(wind_input)):
            if wind_index > 0:
                wind_volume_result = abs(wind_input[wind_index] - wind_input[wind_index - 1]) * 1e9 / turbine_power
                wind_panels_units.append(wind_volume_result)

        # This loop appends the calculation of Wind Volume
        for volume_index in range(len(wind_panels_units)):
            wind_volume.append(wind_panels_units[volume_index] * turbine_volume)

        # This loop appends the calculation of Battery Units
        for battery_index in range(len(battery_input)):
            if battery_index > 0:
                battery_volume_result = abs(battery_input[battery_index] - battery_input[battery_index - 1]) * 1e9 * unit_of_conversion / (52 * solar_system_power)
                battery_units.append(battery_volume_result)

        # This loop appends the calculation of Battery Volume
        for battery_index in range(len(battery_units)):
            battery_volume.append(battery_units[battery_index] * solar_system_volume)

        # This loop appends the calculation of Robot Volume
        for panel_index in range(len(solar_panels_units)):
            robot_volume.append(solar_panels_units[panel_index] * array_of_robots * robot_height * robot_width * robot_length / solar_panels_units[len(solar_panels_units) - 1])

        # This is a Pandas data frame for the Year
        year_index = pd.DataFrame({'Year': ['2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030']})
        # This is a Pandas data frame for the list of Total Solar Volume
        solar_volume_res = pd.DataFrame({'Volume': solar_volume})
        # This is a Pandas data frame for the list of Total Wind Volume
        wind_volume_res = pd.DataFrame({'Volume': wind_volume})
        # This is a Pandas data frame for the list of Total Battery Volume
        battery_volume_res = pd.DataFrame({'Volume': battery_volume})
        # This is a Pandas data frame for the list of Total Robot Volume
        robot_volume_res = pd.DataFrame({'Volume': robot_volume})
        # This concatenates the four Pandas data frames
        Energy_Output_Volume_df = pd.concat([year_index, solar_volume_res, wind_volume_res, battery_volume_res, robot_volume_res], axis = 1)
        # This generates an Excel file for All Energy Producing Panels
        Energy_Output_Volume_df.to_excel("All_energy_producing_panels.xlsx", sheet_name = "All Energy Producing Panels Volume", index = False)

        # This layout visualizes and forecasts the Solar, Wind, Battery, and Robot Volumes
        layout15 = html.Div([
                html.Div([
                    dcc.Graph(id='bar-graph250',
                        figure = go.Figure(
                            data=[go.Bar(x=['2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030'], y = solar_volume, marker={'color': 'blue'}, name = 'Value'),
                                go.Scatter(
                                    x=['2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030'],
                                    y=[val/2 for val in solar_volume],
                                    mode='lines+markers',
                                    line={'color': 'red'},
                                    marker={'symbol': 'circle','size': 10, 'color': 'orange'},
                                    name='Moving Average')],
                            layout=go.Layout(title = 'Demand Model Output of Solar Energy Producing Panels',
                                            title_x=0.5,
                                            xaxis=dict(title='Year'),
                                            yaxis=dict(title='Output Volume (in CBM)'))))
                    ]),
                html.Div([
                    dcc.Graph(id='bar-graph260',
                        figure = go.Figure(
                            data=[go.Bar(x=['2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030'], y = wind_volume, marker={'color': 'blue'}, name = 'Value'),
                                go.Scatter(
                                    x=['2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030'],
                                    y=[val/2 for val in wind_volume],
                                    mode='lines+markers',
                                    line={'color': 'red'},
                                    marker={'symbol': 'circle','size': 10, 'color': 'orange'},
                                    name='Moving Average')],
                            layout=go.Layout(title = 'Demand Model Output of Wind Energy',
                                            title_x=0.5,
                                            xaxis=dict(title='Year'),
                                            yaxis=dict(title='Output Volume (in CBM)'))))
                    ]),
                html.Div([
                    dcc.Graph(id='bar-graph270',
                        figure = go.Figure(
                            data=[go.Bar(x=['2025', '2026', '2027', '2028', '2029', '2030'], y = battery_volume, marker={'color': 'blue'}, name = 'Value'),
                                go.Scatter(
                                    x=['2025', '2026', '2027', '2028', '2029', '2030'],
                                    y=[val/2 for val in battery_volume],
                                    mode='lines+markers',
                                    line={'color': 'red'},
                                    marker={'symbol': 'circle','size': 10, 'color': 'orange'},
                                    name='Moving Average')],
                            layout=go.Layout(title = 'Demand Model Output of Battery Energy',
                                            title_x=0.5,
                                            xaxis=dict(title='Year'),
                                            yaxis=dict(title='Output Volume (in CBM)'))))
                    ]),
                html.Div([
                    dcc.Graph(id='bar-graph280',
                        figure = go.Figure(
                            data=[go.Bar(x=['2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030'], y = robot_volume, marker={'color': 'blue'}, name = 'Value'),
                                go.Scatter(
                                    x=['2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030'],
                                    y=[val/2 for val in robot_volume],
                                    mode='lines+markers',
                                    line={'color': 'red'},
                                    marker={'symbol': 'circle','size': 10, 'color': 'orange'},
                                    name='Moving Average')],
                            layout=go.Layout(title = 'Demand Model Output of Robots',
                                            title_x=0.5,
                                            xaxis=dict(title='Year'),
                                            yaxis=dict(title='Output Volume (in CBM)'))))
                    ]),
                html.Iframe(
                    id='map-graph',
                    src="https://www.google.com/maps/embed/v1/place?key=AIzaSyA2kz9F_7Jw43snykMWvBjdiWySUgf0JmA&q=27.572418511924152,35.536511500684576",
                    style={"width": "100%", "height": "600px"}
                    )
                ])

        # This if statement block indicates the conditions of producing the layouts in the DVI whenever the user navigates among tabs and subtabs
        if main_tab == 'tab-e' and energytab == 'tab-50' and 'energyNEPP' in selected_options:
            return html.Div(layout15)

    # A method that produces the output of Demand Model for the Energy: Nonsolar Energy Production
    def energy_storage_systems_function(self, ess_revenue_input, ess_cost_per_kwh, ess_volume, capex_percentage, energy_volume, recurringCAPEX_percentage, recurring_energy_volume, \
        recurringCAPEX_percentage_cpa, capex_per_cpa, usdcbm_conversion, ess_employment_numbers, volume_energy_storage, EnergyStorageSummary_input_volume, volumePerEmployee_energy_storage, \
        battery_container_inc, EnergyStorageSummary_output_volume, selected_options, main_tab, energytab):

        # This loop appends the calculation of ESS Volume
        for ess_index in range(len(ess_revenue_input)):
            ess_volume.append(ess_revenue_input[ess_index] * 1e6 / ess_cost_per_kwh)
            
        # This loop appends the calculation of Energy Volume
        for revenue_index in range(len(ess_revenue_input)):
            energy_volume.append(ess_revenue_input[revenue_index] * capex_percentage)

        # This loop appends the calculation of Recurring Energy Volume
        for recurring_revenue_index in range(len(ess_revenue_input)):
            recurring_energy_volume.append(energy_volume[recurring_revenue_index] * recurringCAPEX_percentage)
            
        # This loop appends the calculation of CAPEX per CPA
        for recurring_CAPEX_index in range(len(ess_revenue_input)):
            for recurringCPA_index in range(len(recurringCAPEX_percentage_cpa)):
                capex_per_cpa.append(recurring_energy_volume[recurring_CAPEX_index] * recurringCAPEX_percentage_cpa[recurringCPA_index] * 1e6 / usdcbm_conversion[recurringCPA_index])

        # This reshapes the list of CAPEX per CPA to Numpy 2D Arrays
        capex_per_cpa_new = np.reshape(capex_per_cpa, (len(recurringCAPEX_percentage_cpa), len(ess_revenue_input)))

        # This loop includes a nested loop that appends the calculation of input volume of Energy Storage
        for energy_year_index in range(len(ess_employment_numbers)):
            for energyCPA_index in range(len(volume_energy_storage)):
                EnergyStorageSummary_input_volume.append(ess_volume[energy_year_index] * volume_energy_storage[energyCPA_index] + \
                    ess_employment_numbers[energy_year_index] * volumePerEmployee_energy_storage[energyCPA_index] + capex_per_cpa_new[energyCPA_index][energy_year_index])

        # This loop appends the calculation of output volume of Energy Storage
        for ess_index in range(len(ess_revenue_input)):
            EnergyStorageSummary_output_volume.append(ess_volume[ess_index] * battery_container_inc)

        # This is a Pandas data frame for the Year
        year_index = pd.DataFrame({'Year': ['2028', '2029', '2030']})
        # This is a Pandas data frame for the list of output volumes of Energy Storage
        EnergyStorageSummary_output_volume_res = pd.DataFrame({'Volume': EnergyStorageSummary_output_volume})
        # This concatenates the two Pandas data frames
        Energy_Storage_Volume_df = pd.concat([year_index, EnergyStorageSummary_output_volume_res], axis = 1)
        # This generates an Excel file for Energy Storage Systems
        Energy_Storage_Volume_df.to_excel("energy_storage_systems.xlsx", sheet_name = "Energy Storage Systems", index = False)

        # This layout visualizes and forecasts the Energy Storage Systems' Output Volumes
        layout16 = html.Div([
                html.Div([
                    dcc.Graph(id='bar-graph300',
                        figure = go.Figure(
                            data=[go.Bar(x=['2028', '2029', '2030'], y = EnergyStorageSummary_output_volume, marker={'color': 'blue'}, name = 'Value'),
                                go.Scatter(
                                    x=['2028', '2029', '2030'],
                                    y=[val/2 for val in EnergyStorageSummary_output_volume],
                                    mode='lines+markers',
                                    line={'color': 'red'},
                                    marker={'symbol': 'circle','size': 10, 'color': 'orange'},
                                    name='Moving Average')],
                            layout=go.Layout(title = 'Summary Output Volume of Energy Storage Systems',
                                            title_x=0.5,
                                            xaxis=dict(title='Year'),
                                            yaxis=dict(title='Output Volume (in CBM)'))))
                    ]),
                html.Iframe(
                    id='map-graph',
                    src="https://www.google.com/maps/embed/v1/place?key=AIzaSyA2kz9F_7Jw43snykMWvBjdiWySUgf0JmA&q=27.572418511924152,35.536511500684576",
                    style={"width": "100%", "height": "600px"}
                    )
                ])

        # This if statement block indicates the conditions of producing the layouts in the DVI whenever the user navigates among tabs and subtabs
        if main_tab == 'tab-e' and energytab == 'tab-60' and 'energyESS' in selected_options:
            return html.Div(layout16)

    # A method that produces the output of Demand Model for the Energy: Solar
    def solar_function(self, solar_capacity, solar_panel_capacity, number_of_panels, volume_energy_solar, solar_employment_numbers, solarPanel_volume, solarSummary_input_volume, \
        selected_options, input_material_capacity, solarSummary_output_volume, main_tab, energytab):

        # This loop appends the calculation of number of panels
        for solarPanels_index in range(len(solar_capacity)):
            number_of_panels.append(solar_capacity[solarPanels_index] * 1e9 / solar_panel_capacity)

        # This loop appends the calculation of Solar Input Volume
        for solar_capacity_index in range(len(solar_capacity)):
            for volume_energy_solar_index in range(len(volume_energy_solar)):
                solarSummary_input_volume.append(number_of_panels[solar_capacity_index] * solarPanel_volume[volume_energy_solar_index] + solar_employment_numbers[solar_capacity_index] \
                    * volume_energy_solar[volume_energy_solar_index] + np.sum(input_material_capacity) * solar_capacity[solar_capacity_index] / 3)

        # This loop appends the calculation of Solar Output Volume
        for solar_panels_index in range(len(number_of_panels)):
            solarSummary_output_volume.append(number_of_panels[solar_panels_index] * 0.07)

        # This is a Pandas data frame for the Year
        year_index = pd.DataFrame({'Year': ['2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030']})
        # This is a Pandas data frame for the list of output volumes of Solar
        solarSummary_output_volume_res = pd.DataFrame({'Volume': solarSummary_output_volume})
        # This concatenates the two Pandas data frames
        solarSummary_output_volume_df = pd.concat([year_index, solarSummary_output_volume_res], axis = 1)
        # This generates an Excel file for Solar Energy Systems
        solarSummary_output_volume_df.to_excel("solar_energy_systems.xlsx", sheet_name = "Solar Energy Systems", index = False)

        # This layout visualizes and forecasts the Energy Storage Systems' Output Volumes
        layout17 = html.Div([
                html.Div([
                    dcc.Graph(id='bar-graph320',
                        figure = go.Figure(
                            data=[go.Bar(x=['2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030'], y = solarSummary_output_volume, marker={'color': 'blue'}, name = 'Value'),
                                go.Scatter(
                                    x=['2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030'],
                                    y=[val/2 for val in solarSummary_output_volume],
                                    mode='lines+markers',
                                    line={'color': 'red'},
                                    marker={'symbol': 'circle','size': 10, 'color': 'orange'},
                                    name='Moving Average')],
                            layout=go.Layout(title = 'Summary Output Volume of Solar Energy Systems',
                                            title_x=0.5,
                                            xaxis=dict(title='Year'),
                                            yaxis=dict(title='Output Volume (in CBM)'))))
                    ]),
                html.Iframe(
                    id='map-graph',
                    src="https://www.google.com/maps/embed/v1/place?key=AIzaSyA2kz9F_7Jw43snykMWvBjdiWySUgf0JmA&q=27.572418511924152,35.536511500684576",
                    style={"width": "100%", "height": "600px"}
                    )
                ])

        # This if statement block indicates the conditions of producing the layouts in the DVI whenever the user navigates among tabs and subtabs
        if main_tab == 'tab-e' and energytab == 'tab-70' and 'energyS' in selected_options:
            return html.Div(layout17)

    # A method that produces the output of Demand Model for the Energy: Solar
    def wind_function(self, wind_capacity, wind_price, wind_revenues, capacity_per_turbine, number_of_wind_turbines, overall_wind_turbine_output, windSummary_output_volume, \
    selected_options, main_tab, energytab):

        # This loop appends the calculation of wind revenues
        for wind_revenue_index in range(len(wind_capacity)):
            wind_revenues.append(wind_capacity[wind_revenue_index] * wind_price[wind_revenue_index])

        # This loop appends the calculation of number of wind turbines
        for wind_turbines_index in range(len(wind_capacity)):
            number_of_wind_turbines.append(wind_capacity[wind_turbines_index] / capacity_per_turbine)

        # This loop appends the calculation of Wind Output Volume
        for wind_index in range(len(number_of_wind_turbines)):
            windSummary_output_volume.append(number_of_wind_turbines[wind_index] * overall_wind_turbine_output)

        # This is a Pandas data frame for the Year
        year_index = pd.DataFrame({'Year': ['2026', '2027', '2028', '2029', '2030']})
        # This is a Pandas data frame for the list of output volumes of Wind
        windSummary_output_volume_res = pd.DataFrame({'Volume': windSummary_output_volume})
        # This concatenates the two Pandas data frames
        windSummary_output_volume_df = pd.concat([year_index, windSummary_output_volume_res], axis = 1)
        # This generates an Excel file for Wind Energy Systems
        windSummary_output_volume_df.to_excel("wind_turbines.xlsx", sheet_name = "Wind Turbines", index = False)

        # This layout visualizes and forecasts the Energy Storage Systems' Output Volumes
        layout18 = html.Div([
                html.Div([
                    dcc.Graph(id='bar-graph330',
                        figure = go.Figure(
                            data=[go.Bar(x=['2026', '2027', '2028', '2029', '2030'], y = windSummary_output_volume, marker={'color': 'blue'}, name = 'Value'),
                                go.Scatter(
                                    x=['2026', '2027', '2028', '2029', '2030'],
                                    y=[val/2 for val in windSummary_output_volume],
                                    mode='lines+markers',
                                    line={'color': 'red'},
                                    marker={'symbol': 'circle','size': 10, 'color': 'orange'},
                                    name='Moving Average')],
                            layout=go.Layout(title = 'Summary Output Volume of Wind Turbines',
                                            title_x=0.5,
                                            xaxis=dict(title='Year'),
                                            yaxis=dict(title='Output Volume (in CBM)'))))
                    ]),
                html.Iframe(
                    id='map-graph',
                    src="https://www.google.com/maps/embed/v1/place?key=AIzaSyA2kz9F_7Jw43snykMWvBjdiWySUgf0JmA&q=27.572418511924152,35.536511500684576",
                    style={"width": "100%", "height": "600px"}
                    )
                ])

        # This if statement block indicates the conditions of producing the layouts in the DVI whenever the user navigates among tabs and subtabs
        if main_tab == 'tab-e' and energytab == 'tab-80' and 'energyW' in selected_options:
            return html.Div(layout18)

    # A method that produces the output of Demand Model for All NEOM Sectors
    def allSectors_function(self, year, total_volume, main_tab, selected_options):

        # This layout visualizes and forecasts the Output Volumes
        layout19 = html.Div([
                html.Div([
                    dcc.Graph(id='bar-graph340',
                        figure = go.Figure(
                            data=[go.Bar(x=year, y = total_volume, marker={'color': 'blue'}, name = 'Value'),
                                go.Scatter(
                                    x=year,
                                    y=[val/2 for val in total_volume],
                                    mode='lines+markers',
                                    line={'color': 'red'},
                                    marker={'symbol': 'circle','size': 10, 'color': 'orange'},
                                    name='Moving Average')],
                            layout=go.Layout(title = 'Demand Model Output',
                                            title_x=0.5,
                                            xaxis=dict(title='Year'),
                                            yaxis=dict(title='Output Volume (in CBM)'))))
                    ])
                ])

        # This if statement block indicates the conditions of producing the layouts in the DVI whenever the user navigates among tabs and subtabs
        if main_tab == 'tab-med' and 'allSectors' in selected_options:
            return html.Div(layout19)

