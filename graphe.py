import xlsxwriter

def graphiquexls(fname, coordonnees):
    """
    Ecrit les données dans un csv.
    """

    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook(fname+".xlsx")
    worksheet = workbook.add_worksheet()

    # Start from the first cell. Rows and columns are zero indexed.
    worksheet.write(0, 0, "Taille")
    worksheet.write(0, 1, "Fitness")
    row = 1
    col = 0

    # Iterate over the data and write it out row by row.
    for size, solutions in (coordonnees):
        worksheet.write(row, col, size)
        for i in range(len(solutions)):
            worksheet.write(row, col + 1 + i, solutions[i])
        row += 1

    workbook.close()