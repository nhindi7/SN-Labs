# Project Title: NEOM Logistics Data Visualization Interface
# Project Lead: Nezar Hindi
# NEOM Region: NC2
# NEOM Sector: Project Logistics
# Project Lead's Job Title: Supply Chain Data Scientist
# Project Lead's Supervisor: Alan Griffin

# Project Version Number: 1
# Project Status: Frontend Design is under review

# Project Version Number: 2
# Project Status: The whole DVI is under testing

# Project Version Number: 3
# Project Status: Added GPS Feature for each demand model in this DVI

from project_function_collection import * # This line imports all functions and modules from the associated Python source files

# This initiates and creates the server from the backend side of the DVI by using Flask module
server = Flask(__name__)
# This constructs the DVI as a web application by using Dash module
app = dash.Dash(__name__, server=server, external_stylesheets=['styles.css'])

# This indicates an image file of NEOM logo
NEOM_jpg = "NEOM.jpg"
# This indicates an image file of OXAGON logo
OXAGON_jpg = "oxagon.jpg"
# This indicates an image file of OXAGON, NEOM background
OXAGON_theme = "Oxagon_theme.jpg"

# This invokes the function of Crop White Background defined from a collection of project's functions in other Python source file
cropped_neom_image = crop_white_background(NEOM_jpg)
# This produces the output of cropped NEOM logo as a image file in PNG format
cropped_neom_image.save("cropped_neom_logo.png")

# This reads a cropped image file of NEOM logo in PNG format in a binary mode
with open("cropped_neom_logo.png", 'rb') as f:
    image_bytes = f.read()
    encoded_image_neom = base64.b64encode(image_bytes).decode('utf-8')

# This invokes the function of Crop White Background defined from a collection of project's functions in other Python source file
cropped_oxagon_image = crop_white_background(OXAGON_jpg)
# This produces the output of cropped OXAGON logo as a image file in PNG format
cropped_oxagon_image.save("cropped_oxagon_logo.png")

# This reads a cropped image file of OXAGON logo in PNG format in a binary mode
with open("cropped_oxagon_logo.png", 'rb') as f:
    image_bytes = f.read()
    encoded_image_oxagon = base64.b64encode(image_bytes).decode('utf-8')

# This reads an image file of OXAGON background photo in a binary mode
with open(OXAGON_theme, 'rb') as f:
    image_bytes = f.read()
    encoded_theme_oxagon = base64.b64encode(image_bytes).decode('utf-8')

# Update the <head> section
app.title = 'NEOM Logistics DVI'
app.index_string = app.index_string.replace('{%favicon%}', '<link rel="shortcut icon" href="{}" type="image/x-icon">'.format(app.get_asset_url('neom-logo.ico')))

# This layout represents the User Interface (UI) Frontend Design of the DVI
app.layout = html.Div(
    children = [
        # This widget represents the navigational plane in Dash Web App with HTML Style
        html.Nav(
            children=[
                # This widget represents the Link to embed an image file into Dash Web App with HTML Style
                dcc.Link(
                    # This widget represents the image file embedded into Dash Web App with HTML Style
                    html.Img(
                        src='data:image/png;base64,' + encoded_image_neom,
                        style={
                            'width': '10%',
                            'height': '4%',
                            'position': 'relative',
                            'display': 'center'
                        }
                    ),
                    href='/',
                    style={'marginRight': '10px'}
                ),
                # This widget represents the Link to embed an image file into Dash Web App with HTML Style
                dcc.Link(
                    # This widget represents the image file embedded into Dash Web App with HTML Style
                    html.Img(
                        src='data:image/png;base64,' + encoded_image_oxagon,
                        style={
                            'width': '10%',
                            'height': '4%',
                            'position': 'relative',
                            'display': 'center'
                        }
                    ),
                    href='/',
                    style={'marginRight': '10px'}
                )],
            style={'display': 'flex', 
                   'alignItems': 'center',
                   'width': '25%',
                   'height': '25%',
                   'position': 'relative',
                   'display': 'center',
                   'margin-bottom': '250px'
            }),
    # This widget represents the Label as a text embedded into Dash Web App with HTML Style
    html.Label('Choose NEOM Sector or Cluster:', style={'color': 'gold', 'font-weight': 'bold'}),
    # This widget represents a drop-down menu or list encompassing multiple options to include as NEOM sector or cluster
    dcc.Dropdown(
        id='allOptions',
        options=[
            {'label': 'Air Mobility', 'value': 'airMobility'},
            {'label': 'F&B', 'value': 'FB'},
            {'label': 'Hospitality', 'value': 'Hospitality'},
            {'label': 'Energy: Solar Energy Producing Plants', 'value': 'energySEPP'},
            {'label': 'Energy: Hydrogen Facility', 'value': 'energyHF'},
            {'label': 'Energy: Electrolyzers', 'value': 'energyE'},
            {'label': 'Energy: Energy Distribution', 'value': 'energyED'},
            {'label': 'Energy: Non-Solar Energy Producing Plants', 'value': 'energyNEPP'},
            {'label': 'Energy: Energy Storage Systems', 'value': 'energyESS'},
            {'label': 'Energy: Solar', 'value': 'energyS'},
            {'label': 'Energy: Wind', 'value': 'energyW'},
            {'label': 'All NEOM Sectors', 'value': 'allSectors'}
            ],
        value=[],
        multi=True
    ),
    # This widget represents the widget of Division in HTML Style embedded into a data visualization interface by using Python Dash
    html.Div(
        style = {"display": "flex"},
        children = [
            # This widget represents the Label as a text embedded into Dash Web App with HTML Style
            dbc.Label("Demand Data Input", html_for='checkbox', style={'padding': '0px 20px', 'color': 'black'}),
            # This widget represents the Upload Button embedded into Dash Web App with HTML Style
            dcc.Upload(
                id='upload-multi',
                children=html.Div([
                    'Upload'
                ]),
                style={
                    'width': '50px',
                    'height': '15px',
                    'background-color': 'gold',
                    'color': 'white',
                    'padding': '3px 8px',
                    'border-radius': '5px',
                    'display': 'center',
                    'cursor': 'pointer',
                    'position': 'relative',
                    'textAlign': 'center',
                    'marginBottom': '10px',
                    'color': 'black',
                    "margin-right": "20px"
                },
                multiple=True
            )
        ]),
    # This widget represents the tabs and subtabs embedded into Dash Web App with HTML Style
    dcc.Tabs(id = 'main-tab', value = 'tab-am', children = [
        dcc.Tab(label='Air Mobility', value = 'tab-am', children = [
            dcc.Tabs(id='tabs', value='tab-1', children=[
                dcc.Tab(label='Airport CAPEX', value='tab-1', children=[]),
                dcc.Tab(label='Airport OPEX', value='tab-2', children=[]),
                dcc.Tab(label='Airport CAPEX & OPEX', value='tab-3', children=[])
            ])
        ]),
        dcc.Tab(label='F&B', value = 'tab-fb', children = []),
        dcc.Tab(label='Hospitality', value = 'tab-h', children = []),
        dcc.Tab(label='Energy', value = 'tab-e', children = [
            dcc.Tabs(id='tabs2', value='tab-10', children=[
                dcc.Tab(label='Solar Energy Producing Plants', value='tab-10', children=[]),
                dcc.Tab(label='Hydrogen Facility', value='tab-20', children=[]),
                dcc.Tab(label='Electrolyzers', value='tab-30', children=[]),
                dcc.Tab(label='Energy Distribution', value='tab-40', children=[]),
                dcc.Tab(label='Non-Solar Energy Producing Plants', value='tab-50', children=[]),
                dcc.Tab(label='Energy Storage Systems', value='tab-60', children=[]),
                dcc.Tab(label='Solar', value='tab-70', children=[]),
                dcc.Tab(label='Wind', value='tab-80', children=[]),
            ])
        ]),
        dcc.Tab(label='All NEOM Sectors', value = 'tab-med', children = [])
    ]),
    # This widget represents the division of the Dash Web App with HTML Style
    html.Div(id='output-data-upload')
],
    style={
        "background-image": f"url('data:image/jpeg;base64, {encoded_theme_oxagon}')",
        "background-position": "top",
        "background-size": "100% 330px",
        "background-repeat": "no-repeat",
    })

# This function below indicates the main function to be used to initiate the server-side from the backend as well as to feed inputs to all methods of a function collection
@server.route('/')
@app.callback(Output('output-data-upload', 'children'),
               [Input('allOptions', 'value')],
               [Input('upload-multi', 'filename')],
               [Input('main-tab', 'value')],
               [Input('tabs', 'value')],
               [Input('tabs2', 'value')])
def project_testbench_output(selected_options, multiFile, main_tab, amtab, energytab):

    # This creates the object of a project's function collection as an instantiation of its class
    project_items = project_collection()

    # This if statement block executes the method of Airport CAPEX and OPEX with feeding its inputs after meeting the conditions below
    if multiFile is not None and "20230525_AirMobility_template.xlsx" in multiFile and main_tab == 'tab-am' and 'airMobility' in selected_options:

        # This retrieves and reads the Excel file after when the user uploads the file itself
        excel_df = pd.ExcelFile("20230525_AirMobility_template.xlsx", engine='openpyxl')

        # Base Input from the Excel file
        base_input = excel_df.parse('Base input').iloc[4:, 8:16]

        # Input of CPA categories
        CPA_categories = excel_df.parse('Product category CPA level 3').iloc[3:, 3:7]

        # An input of full-time employees
        FTE = excel_df.parse('Retail cbm').iloc[0, 8:16]

        # An input of currency exchange between SAR and USD
        currency_exchange = excel_df.parse('Product category CPA level 3').iloc[1, 4]

        # An input of CPA index
        CPA_column_index = excel_df.parse('Product category CPA level 3').iloc[5:, 1]

        # An input of CPA reference with conversion factors
        CPA_reference = excel_df.parse('Product category CPA level 3').iloc[5:, 1]

        # Another input of full-time employees
        FTE_2 = excel_df.parse('Retail cbm').iloc[2, 6:14].values

        # An input of retail volumes in CBM
        retail_cbm = excel_df.parse('Retail cbm').iloc[3:, 6:14].values

        # This statement returns the return value of Airport CAPEX and OPEX method
        return project_items.airport_CAPEX_OPEX(base_input, currency_exchange, CPA_categories, FTE, CPA_reference, selected_options, CPA_column_index = CPA_column_index, \
            FTE_2 = FTE_2, retail_cbm = retail_cbm, main_tab = main_tab, amtab = amtab)

    # This if statement block executes the method of F&B OPEX with feeding its inputs after meeting the conditions below
    elif multiFile is not None and "20230530_Food  beverages_template.xlsx" in multiFile and main_tab == 'tab-fb' and 'FB' in selected_options:
        
        # This retrieves and reads the Excel file after when the user uploads the file itself
        excel_df = pd.ExcelFile("20230530_Food  beverages_template.xlsx", engine='openpyxl')

        # An input of CPA index
        CPA_column_index = excel_df.parse("Hotel input").iloc[3:, 1].values

        # An input of CPA split index
        CPA_column_split_index = excel_df.parse("OPEX Split").iloc[5:, 6].values

        # An input of conversion factors between budget in USD and volume in CBM
        usd_per_cbm = excel_df.parse("OPEX Split").iloc[5:, 5].values

        # An input of all tourists
        all_tourist = excel_df.parse("Tourists pivots").iloc[3:, 3:13].values

        # An input of all residents
        all_resident = excel_df.parse("Residents pivots").iloc[3:, 3:13].values

        # An input of hotel expenditures
        hotel_spend = excel_df.parse("Hotel input").iloc[3:, 4:14].values
        
        # This statement returns the return value of F&B OPEX method
        return project_items.foodBeverage(all_tourist, all_resident, CPA_column_split_index, usd_per_cbm, hotel_spend, selected_options, CPA_column_index = CPA_column_index, \
            main_tab = main_tab)
        
    # This if statement block executes the method of Hospitality OPEX with feeding its inputs after meeting the conditions below
    elif multiFile is not None and "20230614_Service businesses template.v1.xlsm" in multiFile and main_tab == 'tab-h' and 'Hospitality' in selected_options:

        # This retrieves and reads the Excel file after when the user uploads the file itself
        excel_df = pd.ExcelFile("20230614_Service businesses template.v1.xlsm", engine='openpyxl')

        # An input of CPA index
        CPA_column_index = excel_df.parse('Product category CPA level 3').iloc[5:, 1]

        # An input of conversion factors between budget in USD and volume in CBM
        usd_per_cbm_hosp = excel_df.parse("Product category CPA level 3").iloc[5:, 5].values

        # Base Input from the Excel file
        base_hospit = excel_df.parse("Base input").iloc[3:, 3:11].values

        uk_95weight = 1582546
        uk_96weight = 5590364
        uk_95weight_percentage = 0.59
        uk_96weight_percentage = 0.95

        # Calculation of Hospitality OPEX in GBP by using the given constants above
        uk_opex = ((uk_95weight * uk_95weight_percentage) + (uk_96weight * uk_96weight_percentage)) * 1000
        uk_population = 67e6
        GBPtoUSD = 1.20

        # An empty list of Hospitality OPEX
        hospitality_OPEX = []

        # An empty list of OPEX by region
        opex_to_region = []

        # This list retrieves all the values of Hospitality base input
        value = [x for x in base_hospit.tolist() if x != "value"]

        # This assigns all the values of Hospitality base input to a list of OPEX by region
        opex_to_region = value
        
        # This statement returns the return value of Hospitality OPEX method
        return project_items.hospitality_function(opex_to_region, uk_population, uk_opex, GBPtoUSD, hospitality_OPEX, \
            usd_per_cbm_hosp, selected_options, CPA_column_index = CPA_column_index, main_tab = main_tab)
    
    # This if statement block executes the method of Solar Energy Production with feeding its inputs after meeting the conditions below
    elif multiFile is not None and "20230723_energy producing plants - solar template.v1.xlsm" in multiFile and main_tab == 'tab-e' and energytab == 'tab-10' and 'energySEPP' in selected_options:

        # This retrieves and reads the Excel file after when the user uploads the file itself
        excel_df = pd.ExcelFile("20230723_energy producing plants - solar template.v1.xlsm", engine='openpyxl')

        # Base Input from the Excel file for installed capacities
        installed_capacity = excel_df.parse('Base input').iloc[3, 5:15].values

        panel_capacity = 400

        panel_volume = 0.07

        # An empty list of solar panels' volumes
        solar_panels_volume = []

        # This statement returns the return value of Solar Energy Production method
        return project_items.solar_energy_production(installed_capacity, panel_capacity, panel_volume, solar_panels_volume, selected_options, main_tab = main_tab, energytab = energytab)
    
    # This if statement block executes the method of Hydrogen Facility with feeding its inputs after meeting the conditions below
    elif multiFile is not None and "20230723_hydrogen facility template.v1.xlsm" in multiFile and main_tab == 'tab-e' and energytab == 'tab-20' and 'energyHF' in selected_options:

        # This retrieves and reads the Excel file after when the user uploads the file itself
        excel_df = pd.ExcelFile("20230723_hydrogen facility template.v1.xlsm", engine='openpyxl')

        # Base Input from the Excel file for Hydrogen Facility
        hydrogen_base_input = np.array([50, 150, 250, 100, 100, 100])

        # An empty list of hydrogen capacities
        hydrogen_capacity = []

        # An empty list of employment numbers
        number_of_employees = []

        # An input of volumes per employees in CBM
        volume_per_employee_cbm = excel_df.parse('Product category CPA level 3').iloc[5:, 6].values

        # An input of volumes per employees in USD
        volume_per_employee_usd = excel_df.parse('Product category CPA level 3').iloc[5:, 7].values

        # This statement returns the return value of Hydrogen Facility method
        return project_items.hydrogen_facility_function(hydrogen_capacity, *hydrogen_base_input, selected_options = selected_options, number_of_employees = number_of_employees, \
            volume_per_employee_cbm = volume_per_employee_cbm, volume_per_employee_usd = volume_per_employee_usd, main_tab = main_tab, energytab = energytab)

    # This if statement block executes the method of Electrolyzer with feeding its inputs after meeting the conditions below
    elif multiFile is not None and "20230724_electrolysers template v1.xlsm" in multiFile and main_tab == 'tab-e' and energytab == 'tab-30' and 'energyE' in selected_options:

        # This retrieves and reads the Excel file after when the user uploads the file itself
        excel_df = pd.ExcelFile("20230724_electrolysers template v1.xlsm", engine='openpyxl')

        # An input of revenues from THE LINE
        revenue_line = excel_df.parse("Line-specific metrics").iloc[4, 9:12].values
        
        # An input of revenues from OXAGON
        revenue_oxagon = excel_df.parse("Line-specific metrics").iloc[5, 9:12].values
        
        # An input of number of electrolyzers
        number_of_electrolyzers = excel_df.parse("Line-specific metrics").iloc[6, 9:12].values

        # An input of number of electrolyzer cells
        number_of_cells = excel_df.parse("Line-specific metrics").iloc[7, 9:12].values

        # An input of electrolyzer capacities
        electrolyzer_capacity = excel_df.parse("Combined metrics").iloc[9, 9:12].values

        # An input of number of electrolyzer units
        output_of_electrolyzer_units = excel_df.parse("Product category CPA level 3").iloc[5:, 8].values

        # An input of number of hydrogen electrolyzers
        number_of_hydrogen_electrolyzers = excel_df.parse("Base input").iloc[9, 10:13].values

        # An empty list of hydrogen electrolyzer units
        hydrogen_electrolyzer_units = []

        # An empty list of hydrogen electrolyzer cells
        hydrogen_electrolyzer_cells = []

        # An empty list of total electrolyzer capacity
        total_electrolyzer_capacity = []

        # An empty list of output volumes from OXAGON
        summary_output_volume_oxagon = []

        # An empty list of output volumes from THE LINE
        summary_output_volume_line = []

        # This statement returns the return value of Electrolyzer method
        return project_items.electrolyzer_function(hydrogen_electrolyzer_units, number_of_electrolyzers, revenue_oxagon, revenue_line, hydrogen_electrolyzer_cells, number_of_cells, \
            total_electrolyzer_capacity, electrolyzer_capacity, number_of_hydrogen_electrolyzers, output_of_electrolyzer_units, selected_options, summary_output_volume_oxagon, \
            summary_output_volume_line, main_tab = main_tab, energytab = energytab)
        
    # This if statement block executes the method of Energy Distribution with feeding its inputs after meeting the conditions below
    elif multiFile is not None and "20230724_energy distribution template v1.xlsm" in multiFile and main_tab == 'tab-e' and energytab == 'tab-40' and 'energyED' in selected_options:

        # This retrieves and reads the Excel file after when the user uploads the file itself
        excel_df = pd.ExcelFile("20230724_energy distribution template v1.xlsm", engine='openpyxl')

        # An input of total percentage recurring CAPEX
        total_percentage_recurring_capex = excel_df.parse("Product category CPA level 3").iloc[4:, 8].values

        # An input of Energy Distribution CAPEX
        energy_distribution_capex_sar = excel_df.parse("Base input").iloc[4, 4:11].values

        # This mathematical operation converts Energy Distribution CAPEX from SAR to USD
        energy_distribution_capex_usd = 0.27 * energy_distribution_capex_sar

        # This mathematical operation computes Energy Distribution Recurring CAPEX in USD
        energy_distribution_recurCapex_usd = 0.025 * energy_distribution_capex_usd

        # An empty list of recurring CAPEX breakdown
        recurring_Capex_breakdown = []
        
        # An input of Energy Distribution OPEX
        energy_distribution_opex_sar = excel_df.parse("Base input").iloc[3, 4:11].values

        # This mathematical operation computes Energy Distribution OPEX in SAR
        energy_distribution_opex_operating = 0.64 * energy_distribution_opex_sar

        # This mathematical operation computes the non-labor costs in USD
        nonlabor_costs = 0.43 * energy_distribution_opex_operating

        # An input of Adjusted Power Grid
        adjusted_power_grid = excel_df.parse("Product category CPA level 3").iloc[4:, 7].values

        # An empty list of OPEX per CPA
        opex_per_cpa = []

        # This statement returns the return value of Energy Distribution method
        return project_items.energy_distribution_function(energy_distribution_recurCapex_usd, total_percentage_recurring_capex, recurring_Capex_breakdown, energy_distribution_capex_usd, \
            nonlabor_costs, adjusted_power_grid, opex_per_cpa, energy_distribution_opex_sar, selected_options, main_tab, energytab)
    
    # This if statement block executes the method of Nonsolar Energy Production with feeding its inputs after meeting the conditions below
    elif multiFile is not None and "20230724_energy producing plants - non-solar.xlsm" in multiFile and main_tab == 'tab-e' and energytab == 'tab-50' and 'energyNEPP' in selected_options:

        # This retrieves and reads the Excel file after when the user uploads the file itself
        excel_df = pd.ExcelFile("20230724_energy producing plants - non-solar.xlsm", engine='openpyxl')

        # A base input of Solar Energy
        solar_input = excel_df.parse("Base input").iloc[3, 5:14].values

        # A base input of Wind Energy
        wind_input = excel_df.parse("Base input").iloc[4, 5:14].values

        # A base input of Battery Energy
        battery_input = excel_df.parse("Base input").iloc[5, 7:14].values

        panel_capacity = 400

        panel_volume = 0.07

        unit_of_conversion = 4

        density_of_steel = 7700

        solar_panel_length = 1.69

        solar_panel_width = 1.04

        turbine_power = 5e6

        turbine_volume = 5538

        solar_system_power = 1000

        solar_system_volume = 0.0127

        robot_length = 1.45

        robot_width = 1.30

        robot_height = 0.35

        array_of_robots = 5000

        # An empty list of solar panels' units
        solar_panels_units = []

        # An empty list of solar volumes
        solar_volume = []

        # An empty list of wind panels' units
        wind_panels_units = []

        # An empty list of wind volumes
        wind_volume = []

        # An empty list of battery units
        battery_units = []

        # An empty list of battery volumes
        battery_volume = []

        # An empty list of robot volumes
        robot_volume = []

        # This statement returns the return value of Nonsolar Energy Production method
        return project_items.nonsolar_energy_production_function(solar_input, solar_panels_units, panel_capacity, solar_volume, solar_panel_length, solar_panel_width, unit_of_conversion, \
            density_of_steel, wind_input, turbine_power, wind_panels_units, turbine_volume, wind_volume, battery_input, solar_system_power, battery_units, solar_system_volume, \
            battery_volume, robot_volume, array_of_robots, robot_height, robot_width, robot_length, selected_options, main_tab = main_tab, energytab = energytab)

    # This if statement block executes the method of Energy Storage Systems with feeding its inputs after meeting the conditions below
    elif multiFile is not None and "20230724_Energy Storage Systems template v1.xlsm" in multiFile and main_tab == 'tab-e' and energytab == 'tab-60' and 'energyESS' in selected_options:

        # This retrieves and reads the Excel file after when the user uploads the file itself
        excel_df = pd.ExcelFile("20230724_Energy Storage Systems template v1.xlsm", engine='openpyxl')

        # A base input of ESS Revenue
        ess_revenue_input = excel_df.parse("Base input").iloc[3, 9:12].values

        # A base input of ESS Employment Numbers
        ess_employment_numbers = excel_df.parse("Base input").iloc[4, 9:12].values

        ess_cost_per_kwh = 380

        # An empty list of ESS volumes
        ess_volume = []

        capex_percentage = 0.14

        recurringCAPEX_percentage = 0.025

        battery_container_inc = 0.0127

        # An empty list of Energy volumes
        energy_volume = []

        # An empty list of Recurring Energy volumes
        recurring_energy_volume = []

        # An empty list of CAPEX per CPAs
        capex_per_cpa = []

        # An empty list of Energy Storage Input Volumes
        EnergyStorageSummary_input_volume = []

        # An empty list of Energy Storage Output Volumes
        EnergyStorageSummary_output_volume = []

        # An input of recurring CAPEX percentage per CPA
        recurringCAPEX_percentage_cpa = excel_df.parse("Product category CPA level 3").iloc[4:, 9].values

        # An input of USD to CBM conversion
        usdcbm_conversion = excel_df.parse("Product category CPA level 3").iloc[4:, 5].values

        # An input of Volume Energy Storage
        volume_energy_storage = excel_df.parse("Product category CPA level 3").iloc[4:, 8].values

        # An input of Volume per employee Energy Storage
        volumePerEmployee_energy_storage = excel_df.parse("Product category CPA level 3").iloc[4:, 6].values

        # This statement returns the return value of Energy Storage Systems method
        return project_items.energy_storage_systems_function(ess_revenue_input, ess_cost_per_kwh, ess_volume, capex_percentage, energy_volume, recurringCAPEX_percentage, recurring_energy_volume, \
            recurringCAPEX_percentage_cpa, capex_per_cpa, usdcbm_conversion, ess_employment_numbers, volume_energy_storage, EnergyStorageSummary_input_volume, \
            volumePerEmployee_energy_storage, battery_container_inc, EnergyStorageSummary_output_volume, selected_options, main_tab = main_tab, energytab = energytab)

    # This if statement block executes the method of Solar Energy with feeding its inputs after meeting the conditions below
    elif multiFile is not None and "20230724_solar template v1.xlsm" in multiFile and main_tab == 'tab-e' and energytab == 'tab-70' and 'energyS' in selected_options:

        # This retrieves and reads the Excel file after when the user uploads the file itself
        excel_df = pd.ExcelFile("20230724_solar template v1.xlsm", engine='openpyxl')

        # A base input of Solar Capacity
        solar_capacity = excel_df.parse("Base input").iloc[4, 4:12].values

        solar_panel_capacity = 400

        # An empty list of number of panels
        number_of_panels = []

        # An input of Solar Panel Volume
        solarPanel_volume = excel_df.parse("Product category CPA level 3").iloc[4:, 6].values

        # An input of Solar Employment Numbers
        solar_employment_numbers = excel_df.parse("Base input").iloc[3, 4:12].values

        # An input of Solar Energy Volume
        volume_energy_solar = excel_df.parse("Product category CPA level 3").iloc[4:, 8].values

        # An input of Material Capacity
        input_material_capacity = excel_df.parse("Assumptions").iloc[31:44, 5].values

        # An empty list of Input Solar Volume
        solarSummary_input_volume = []

        # An empty list of Output Solar Volume
        solarSummary_output_volume = []

        # This statement returns the return value of Solar Energy method
        return project_items.solar_function(solar_capacity, solar_panel_capacity, number_of_panels, volume_energy_solar, solar_employment_numbers, solarPanel_volume, solarSummary_input_volume, \
            selected_options, input_material_capacity, solarSummary_output_volume, main_tab = main_tab, energytab = energytab)

    # This if statement block executes the method of Wind Energy with feeding its inputs after meeting the conditions below
    elif multiFile is not None and "20230724_wind template v1.xlsm" in multiFile and main_tab == 'tab-e' and energytab == 'tab-80' and 'energyW' in selected_options:

        # This retrieves and reads the Excel file after when the user uploads the file itself
        excel_df = pd.ExcelFile("20230724_wind template v1.xlsm", engine='openpyxl')

        # A base input of Wind Capacity
        wind_capacity = excel_df.parse("Base input").iloc[3, 7:12].values

        # A base input of Wind Price
        wind_price = excel_df.parse("Base input").iloc[4, 7:12].values

        # An empty list of wind revenues
        wind_revenues = []

        capacity_per_turbine = 5

        # An empty list of number of wind turbines
        number_of_wind_turbines = []

        overall_wind_turbine_output = 5538.2

        # An empty list of Output Wind Volume
        windSummary_output_volume = []

        # This statement returns the return value of Wind Energy method
        return project_items.wind_function(wind_capacity, wind_price, wind_revenues, capacity_per_turbine, number_of_wind_turbines, overall_wind_turbine_output, windSummary_output_volume, \
            selected_options, main_tab = main_tab, energytab = energytab)

    # This if statement block executes the method of allSectors with feeding its inputs after meeting the conditions below
    elif multiFile is not None and "20231102_Demand_output.xlsx" in multiFile and main_tab == 'tab-med' and 'allSectors' in selected_options:
        
        # This retrieves and reads the Excel file after when the user uploads the file itself
        excel_df = pd.ExcelFile("20231102_Demand_output.xlsx", engine='openpyxl')

        # An input of all years from 2025 to 2055
        year = excel_df.parse("20231102_Demand_output").iloc[0:31, 10].values

        # An input of total volumes
        total_volume = excel_df.parse("20231102_Demand_output").iloc[0:31, 11].values

        # This statement returns the return value of allSectors method
        return project_items.allSectors_function(year, total_volume, main_tab, selected_options)
    
    # This if statement block executes if none of the above conditions have been met
    else:
        # This statement returns the return value of empty Divison within Dash Web App in HTML Style
        return html.Div([])

# This if statement block executes the main function in the server-side from the backend by using both Flask and Dash modules
if __name__ == '__main__':
    app.run_server(host='127.0.0.1', debug=True, port=2024)