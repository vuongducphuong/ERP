# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import json

from odoo import http
from odoo.http import request
from odoo.tools import misc
from odoo.exceptions import ValidationError

FILE_NAME_MODEL_MAPPING = {
    '6. Tồn kho vật tư hàng hóa.xls': 'account.ex.ton.kho.vat.tu.hang.hoa',
    '3. Công nợ khách hàng.xls': 'cong.no.khach.hang',
    '4. Công nợ nhà cung cấp.xls': 'cong.no.nha.cung.cap',
    '5. Công nợ nhân viên.xls': 'cong.no.nhan.vien',
    '1. Số dư tài khoản.xls': 'so.du.tai.khoan',
    '2. Số dư TK ngân hàng.xls': 'so.du.tk.ngan.hang',
	'7. Chi phí dở dang - Công trình.xls': 'chi.phi.do.dang.cong.trinh',
	'8. Chi phí dở dang - Đối tượng THCP.xls': 'chi.phi.do.dang.doi.tuong.thcp',
	'9. Chi phí dở dang - Đơn hàng.xls': 'chi.phi.do.dang.don.hang',
	'10. Chi phí dở dang - Hợp đồng.xls': 'chi.phi.do.dang.hop.dong',
    }

class ImportController(http.Controller):

    @http.route('/base_import_ex/set_multi_file', methods=['POST'])
    def set_multi_file(self, file, import_id, jsonp='callback'):
        import_id = int(import_id)
        files = request.httprequest.files.getlist('file')
        parent_import = request.env['base_import_ex.import_excels'].browse(import_id)
        # Trường hợp tải lại
        request.env['base_import_ex.import_excels'].search([('parent_id', '=', import_id)]).unlink()
        if parent_import.res_model:
            for f in files:
                request.env['base_import_ex.import_excels'].create({
                    'file': f.read(),
                    'file_name': f.filename,
                    'file_type': f.content_type,
                    'res_model': '.'.join([parent_import.res_model, 'excel']),
                    'parent_id': import_id,
                })
        else:
            for f in files:
                res_model = FILE_NAME_MODEL_MAPPING.get(f.filename)
                if res_model:
                    request.env['base_import_ex.import_excels'].create({
                        'file': f.read(),
                        'file_name': f.filename,
                        'file_type': f.content_type,
                        'res_model': res_model,
                        'parent_id': import_id,
                    })
                else:
                    return False
                    # raise ValidationError("""
                    # Tên file %s không hợp lệ. Danh sách file có thể nhập khẩu:/

                    #     '1. Số dư tài khoản.xls/
                    #     '2. Số dư TK ngân hàng.xls/
                    #     '3. Công nợ khách hàng.xls/
                    #     '4. Công nợ nhà cung cấp.xls/
                    #     '5. Công nợ nhân viên.xls/
                    #     '6. Tồn kho vật tư hàng hóa.xls/""" % f.filename)

        return 'window.top.%s(%s)' % (misc.html_escape(jsonp), json.dumps({'result': True}))


    # Todof: Kiểm tra lại với trường hợp import nhiều file
    @http.route('/base_import_ex/set_single_file', methods=['POST'])
    def set_single_file(self, file, import_id, jsonp='callback'):
        import_id = int(import_id)
        files = request.httprequest.files.getlist('file')
        # Trường hợp tải lại
        request.env['base_import_ex.import'].search([('parent_id', '=', import_id)]).unlink()
        for f in files:
            request.env['base_import_ex.import'].create({
                'file': f.read(),
                'file_name': f.filename,
                'file_type': f.content_type,
                'res_model': f.filename.replace('.xls',''),
                'parent_id': import_id,
            })

        return 'window.top.%s(%s)' % (misc.html_escape(jsonp), json.dumps({'result': True}))
