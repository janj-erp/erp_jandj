# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

import time
from datetime import datetime
import tempfile
import binascii
from datetime import date, datetime
from odoo.exceptions import Warning, UserError
from odoo import models, fields, exceptions, api, _
import logging

_logger = logging.getLogger(__name__)
import io

try:
    import xlrd
except ImportError:
    _logger.debug('Cannot `import xlrd`.')
try:
    import csv
except ImportError:
    _logger.debug('Cannot `import csv`.')
try:
    import xlwt
except ImportError:
    _logger.debug('Cannot `import xlwt`.')
try:
    import cStringIO
except ImportError:
    _logger.debug('Cannot `import cStringIO`.')
try:
    import base64
except ImportError:
    _logger.debug('Cannot `import base64`.')


class ImportChartAccount(models.Model):
    _name = "import.chart.account"
    _description = "Chart of Account"

    file_select = fields.Binary(string="Select Excel File")
    import_option = fields.Selection([('csv', 'CSV File'), ('xls', 'XLS File')], string='Select', default='xls')

    def imoport_file(self):
        # -----------------------------
        if self.import_option == 'csv':
            raise UserError(_("Invalid file! (.xlsx files are allowed)"))

        # ---------------------------------------
        elif self.import_option == 'xls':
            try:
                fp = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
                fp.write(binascii.a2b_base64(self.file_select))
                fp.seek(0)
                values = {}
                workbook = xlrd.open_workbook(fp.name)
                sheet = workbook.sheet_by_index(0)
            except:
                raise UserError(_("Invalid file! (.xlsx files are allowed)"))

            cols = 0
            row_no = 0
            variant_col = 3
            header = []
            products = self.env['product.template'].browse(-1)
            while row_no < sheet.nrows:
                val = {}
                if row_no == 0:
                    line = list(
                        map(lambda row: isinstance(row.value, bytes) and row.value.encode('utf-8') or str(row.value),
                            sheet.row(row_no)))
                    header = line
                    # print(row_no)
                    print('headers', len(line), line)
                    cols = len(line)
                    while variant_col < len(line):
                        if 'variants'.lower() in line[variant_col].lower():
                            break
                        variant_col += 1
                    # print(variant_col)
                else:
                    line = list(
                        map(lambda row: isinstance(row.value, bytes) and row.value.encode('utf-8') or str(row.value),
                            sheet.row(row_no)))
                    # print(row_no)
                    print('values', line)
                    if line[0].strip() != '' and line[1].strip() != '':
                        product = self.env['product.template'].search(
                            [('name', '=ilike', line[1].strip()), ('default_code', '=ilike', line[0].strip())])
                        # product2 = self.env['product.template'].search(
                        #     [('name', '=ilike', line[1].strip())])
                        # print(product, product2, product2.default_code, line[0])
                        # print(product.default_code, line[0])
                        # print(product.default_code == line[0])
                        if product:
                            print(len(product), 'Exists')
                            print(product.name, product.default_code)
                        else:
                            product = self.env['product.template'].create({'name': line[1],
                                                                           'default_code': line[0],
                                                                           'detailed_type': 'product',
                                                                           'available_in_pos': 1})
                            if line[2].strip() != '':
                                line[2] = line[2].upper().strip()
                                categ = self.env['product.category'].search([('name', '=', line[2])], limit=1)
                                if categ:
                                    product.categ_id = categ
                                else:
                                    product.categ_id = self.env['product.category'].create({'name': line[2]})

                                pos_categ = self.env['pos.category'].search([('name', '=', line[2])], limit=1)
                                if pos_categ:
                                    product.pos_categ_id = pos_categ
                                else:
                                    product.pos_categ_id = self.env['pos.category'].create({'name': line[2]})
                            print("1", product.name, product.default_code)

                        line[3] = line[3].strip().split('.')[0]
                        if line[3].isnumeric():
                            product.list_price = line[3]
                            # print("2", product.name, product.default_code)

                        for i in range(4, variant_col):
                            print(header[i], line[i])
                            if line[i].strip() != '':
                                tag_name = header[i].strip().capitalize() + ": " + line[i].strip().upper()
                                tag = self.env['product.tags'].search([('name', '=ilike', tag_name)])
                                if tag:
                                    product.tag_ids += tag
                                else:
                                    product.tag_ids += self.env['product.tags'].create({'name': tag_name})

                        if 'yes' in line[variant_col].lower().strip():
                            # print('yes')
                            i = variant_col + 1
                            while 'barcode' not in header[i].lower() and i < len(line):
                                print(i, product.name, product.default_code)
                                if line[i].strip() != '':
                                    attribute = self.env['product.attribute'].search([('name', '=ilike', header[i].strip())])
                                    if not attribute:
                                        attribute = self.env['product.attribute'].create({'name': header[i].upper().strip()})
                                    values = list(map(lambda a: a.upper().strip(), line[i].split(',')))
                                    # print(attribute, values)
                                    attribute_values = self.env['product.attribute.value'].search([('name', '=', '2')])
                                    for val in values:
                                        # print(val.lower(), list(map(lambda a: a.lower().strip(),
                                        #                            attribute.value_ids.mapped('name'))))
                                        if val.lower() in list(map(lambda a: a.lower().strip(),
                                                                   attribute.value_ids.mapped('name'))):
                                            attr_val = attribute.value_ids.filtered(lambda a: a.name.upper() == val.upper())[:1]
                                            print(attr_val)
                                            attribute_values += attr_val
                                        else:
                                            attribute_values += self.env['product.attribute.value'].create({'name': val,
                                                                                                            'attribute_id': attribute.id})

                                    # 'product.attribute.value'
                                    # print(attribute.name.lower().strip(),
                                    #       list(map(lambda a: a.name.lower().strip(),
                                    #                product.attribute_line_ids.mapped('attribute_id')))
                                    #       )
                                    if attribute.name.lower().strip() in \
                                            list(map(lambda a: a.name.lower().strip(),
                                                     product.attribute_line_ids.mapped('attribute_id'))):
                                        attr = product.attribute_line_ids.filtered(lambda a: a.attribute_id.name.lower().strip() == attribute.name.lower().strip())[:1]
                                        # print(attr)
                                        attr.value_ids += attribute_values
                                    else:
                                        self.env['product.template.attribute.line'].create({'attribute_id': attribute.id,
                                                                                            'value_ids':
                                                                                                [(6, 0, attribute_values.ids)],
                                                                                            'product_tmpl_id': product.id})
                                    # print(product.attribute_line_ids)
                                    # line = self.env['product.template.attribute.line'].create({'attribute_id': attribute.id})
                                    # line.value_ids = attribute_values
                                    # product.attribute_line_ids += line
                                i += 1
                            # while row_no < sheet.nrows - 1:
                            #     line = list(
                            #         map(lambda row: isinstance(row.value, bytes) and row.value.encode('utf-8') or str(
                            #             row.value),
                            #             sheet.row(row_no + 1)))
                            #     if line[0].strip() == '' and line[1].strip() == '':
                            #         row_no += 1
                            #
                            #     else:
                            #         break
                        products += product

                        product.default_code = line[0]
                        print(product.name, product.default_code)
                        # raise UserError(_("Please select any one from xls or csv formate!"))

                # print(product.name, product.default_code)
                # print('row_no: ', row_no, ', ', sheet.nrows)

                row_no += 1
                # print('row_no: ', row_no, ', ', sheet.nrows)


            if len(products) > 1:
                #Generate a new excel file
                workbook = xlwt.Workbook()

                worksheet = workbook.add_sheet('Product Variant Template')
                font = xlwt.Font()
                font.bold = True
                for_leftb = xlwt.easyxf(
                    "font: bold 1, color black;")
                for_left = xlwt.easyxf(
                    "font: color black;")
                worksheet.col(2).width = 10000
                worksheet.col(3).width = 10000
                worksheet.write(0, 0, 'Database ID', for_leftb)
                worksheet.write(0, 1, 'Item Code', for_leftb)
                worksheet.write(0, 2, 'Product Variant', for_leftb)
                worksheet.write(0, 3, 'Tags', for_leftb)
                worksheet.write(0, 4, 'Quantity', for_leftb)
                start_from = 0
                # print(products)
                for product in products[1:]:
                    variants = self.env['product.product'].search([('product_tmpl_id', '=', product.id)])
                    # print('\n\n\n\n\n\n', variants)
                    for i, var in enumerate(variants):
                        worksheet.write(1+i+start_from, 0, var.id, for_left)
                        worksheet.write(1+i+start_from, 1, product.default_code, for_left)
                        worksheet.write(1+i+start_from, 2, var.display_name, for_left)
                        print(product.tag_ids.mapped('name'))
                        worksheet.write(1+i+start_from, 3, ', '.join(product.tag_ids.mapped('name')), for_left)
                    start_from += i + 1
                    # print(start_from)

                # worksheet.write(1, 0, '', for_left_not_bold)
                # worksheet.write(row, 1, '', for_left_not_bold)

                fp = io.BytesIO()
                workbook.save(fp)
                product_id = self.env['product.excel.extended'].create(
                    {'excel_file': base64.encodebytes(fp.getvalue()), 'file_name': 'ProductVariantTemplate.xlsx'})
                fp.close()

                return {
                    'view_mode': 'form',
                    'res_id': product_id.id,
                    'res_model': 'product.excel.extended',
                    'view_type': 'form',
                    'type': 'ir.actions.act_window',
                    'context': self._context,
                    'target': 'new',
                }

    def import_stock(self):
        picking = self.env['stock.picking'].browse(self.env.context.get('active_id'))
        # print(picking)

        try:
            fp = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
            fp.write(binascii.a2b_base64(self.file_select))
            fp.seek(0)
            values = {}
            workbook = xlrd.open_workbook(fp.name)
            sheet = workbook.sheet_by_index(0)
        except:
            raise UserError(_("Invalid file!"))
        for row_no in range(sheet.nrows):
            line = list(
                map(lambda row: isinstance(row.value, bytes) and row.value.encode('utf-8') or str(row.value),
                    sheet.row(row_no)))
            # print(line)
            if row_no > 0:
                if line[0] == '':
                    raise UserError(_('Please enter the product\'s ID for row :' + str(row_no+1)))
                # print(line[0], type(line[0]))
                # print(int(line[0].strip().split('.')[0]))
                line[0] = line[0].strip().split('.')[0]
                if not line[0].isnumeric():
                    raise UserError(_('Product\'s ID not an integer for row :' + str(row_no+1)))
                line[4] = line[4].strip().split('.')[0]
                if line[4] == '':
                    line[4] = '0'
                if not line[4].isnumeric():
                    raise UserError(_('Quantity not an integer row :' + str(row_no+1)))
                else:
                    product = self.env['product.product'].browse(int(line[0]))
                    if not product:
                        raise UserError(_('Could not find Product for row :' + str(row_no + 1)))
                    picking.move_ids_without_package += self.env['stock.move'].create({'name': 'POS stock request',
                                                                                   'product_uom': product.uom_id.id,
                                                                                   'product_id': product.id,
                                                                                   'product_uom_qty': int(line[4]),
                                                                                   'company_id': picking.company_id.id,
                                                                                   'location_id': picking.location_id.id,
                                                                                   'location_dest_id': picking.location_dest_id.id,
                                                                                   'date': fields.Date.today()})

                # if line[0]:
                #     product = self.env['product.product'].browse()


class ProductExcelExtended(models.Model):
    _name = 'product.excel.extended'
    _description = "Product Excel Extended"

    excel_file = fields.Binary('Download Report :- ')
    file_name = fields.Char('Excel File', size=64)
