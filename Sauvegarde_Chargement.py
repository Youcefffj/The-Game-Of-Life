# Sauvegarde_Chargement.py
def sauvegarder_grille(cells, file_name):
    with open(file_name, 'w') as file:
        for row in cells:
            for cell in row:
                file.write(str(cell))
            file.write('\n')


def charger_grille(file_name,cells):

    with open(file_name, 'r') as file:
        for row_index, line in enumerate(file):
            row_values = line.strip().split('.')
            for i in range (min(len(row_values), 50)):
                cells[row_index][i] = int(row_values[i])
    return cells
