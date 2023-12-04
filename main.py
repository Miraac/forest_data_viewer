import text_interface as ui
print('This program analyzing and showing results for data from BDL about Polish forests'
      '\nRequied libraries: Pandas and Geopandas(if choose shapefile)')
input('If libraries arent installed the program will close.\nClick enter to continue.')
import sys


print('python ver p: 3.9.13 -> o: ',sys.version,' ')
# dane = pd.read_csv('f_area_type_dic.txt', delimiter=' ')


data, language = ui.importFileInterface()
data, k_col = ui.choose_column_names_ui(data, language)
ui.main_interface(data, k_col)
