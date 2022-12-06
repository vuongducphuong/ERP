from odoo import api, models

class UY_NHIEM_CHI_SHB_REPORT(models.AbstractModel):
    _name = 'report.account_ex.template_account_ex_phieu_chi_unc_shb'

    @api.model
    def get_report_values(self, docids, data=None):
        records = self.env['account.ex.phieu.thu.chi'].browse(docids)     

        for record in records:
            if record.TAI_KHOAN_CHI_GUI_ID.DIA_CHI_CN ==False:
                record.TAI_NGAN_HANG_MAU_IN = record.TEN_TK_CHI  
            else:
                record.TAI_NGAN_HANG_MAU_IN =  record.TEN_TK_CHI  + "-" + record.TAI_KHOAN_CHI_GUI_ID.DIA_CHI_CN
            
                       
        return {
            'doc_ids': docids,
            'doc_model': 'account.ex.phieu.thu.chi',
            'docs': records,
            'data': data,
        }
    