import csv

import xlsxwriter


def graphique(fname, coordonnees) :
    file = open(fname+".csv", "w")
    try:
        writer = csv.writer(file)
        writer.writerow(("Taille", "Fitness"))
        """for coord in coordonnees:
            writer.writerow(coord)
            """
    finally:
        file.close()

def graphiquexls(fname, coordonnees):
    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook(fname+".xlsx")
    worksheet = workbook.add_worksheet()

    # Start from the first cell. Rows and columns are zero indexed.

    worksheet.write(0, 0, "Taille")
    worksheet.write(0, 1, "Fitness")
    row = 1
    col = 0

    # Iterate over the data and write it out row by row.
    for size, fitness in (coordonnees):
        worksheet.write(row, col, size)
        worksheet.write(row, col + 1, fitness)
        row += 1

    workbook.close()