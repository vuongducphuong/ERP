from odoo import api, models
from collections import Counter 

class CHUNG_TU_GHI_SO_REPORT(models.AbstractModel):
    _name = 'report.tong_hop.template_tong_hop_chung_tu_ghi_so'

    @api.model
    def get_report_values(self, docids, data=None):
        records = self.env['tong.hop.chung.tu.ghi.so'].browse(docids)
        arr = []
        for record in records:
            for detail in record.TONG_HOP_CHUNG_TU_GHI_SO_CHI_TIET_IDS:
                arr.append(detail.SO_CHUNG_TU)
      
            a = len(Counter(arr).keys()) 
        record.CHUNG_TU_GOC_MAU_IN = a
        return {
            'doc_ids': docids,
            'doc_model': 'tong.hop.chung.tu.ghi.so',
            'docs': records,
            'data': data,
        }