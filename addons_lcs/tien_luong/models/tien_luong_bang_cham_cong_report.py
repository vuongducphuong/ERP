# -*- coding: utf-8 -*-
# © 2018 GDC COMPANY ALL RIGHTS RESERVED

from odoo import api, models, fields, helper

class TIEN_LUONG_BANG_CHAM_CONG_REPORT(models.AbstractModel):
    _name = 'report.tien_luong.template_tien_luong_bang_cham_cong'

    @api.model
    def get_report_values(self, docids, data=None):
        records = self.env['tien.luong.bang.cham.cong.chi.tiet.master'].browse(docids)
        grouped_datas = {}
        for record in records:
            grouped_data = {}
            for line in record.TIEN_LUONG_BANG_CHAM_CONG_CHI_TIET_DETAIL_IDS:
                line_data = helper.Obj.convert_obj_to_dict(line)
                line_data['MA_NHAN_VIEN'] = line_data.get('MA_NHAN_VIEN').MA
                don_vi = line.DON_VI_ID.id
                if not grouped_data.get(don_vi):
                    grouped_data[don_vi] = {
                        'data': [],
                        'sum': 0,
                        'TEN_DON_VI': line.DON_VI_ID.TEN_DON_VI or '',
                    }
                grouped_data[don_vi]['data'] += [line_data]
                grouped_data[don_vi]['sum'] += line_data.get('SO_CONG_HUONG', 0)
            grouped_datas[record.id] = grouped_data
        return {
            'doc_ids': docids,
            'doc_model': 'tien.luong.bang.cham.cong.chi.tiet.master',
            'docs': records,
            'data': data,
            'grouped_datas': grouped_datas,
        }