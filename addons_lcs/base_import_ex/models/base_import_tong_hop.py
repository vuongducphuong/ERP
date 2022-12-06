# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, helper

MODULE = 'base_import_ex'


class Import(models.TransientModel):
    _inherit = 'base_import_ex.import'

    # Chứng từ ghi sổ

    def _import_GLVoucherList(self, tag):
        rec_model = 'tong.hop.chung.tu.ghi.so'
        res = { }
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefID':
                rec_id = child.text
            elif child.tag == 'RefType':
                res['LOAI_CHUNG_TU'] =  int(child.text)
            elif child.tag == 'BranchID':
                rid=self.env.ref('{}.{}'.format(MODULE,child.text), False)
                if rid:
                    res['CHI_NHANH_ID'] = rid.id
            elif child.tag == 'RefDate':
                res['NGAY_CHUNG_TU'] = child.text
            elif child.tag == 'RefNo':
                res['SO_CHUNG_TU'] = child.text
            elif child.tag == 'JournalMemo':
                res['DIEN_GIAI'] = child.text
            elif child.tag == 'TotalAmount':
                res['TONG_TIEN'] = float(child.text)

        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)

    # Chứng từ ghi sổ chi tiết
    def _import_GLVoucherListDetail(self,tag):
        rec_model = 'tong.hop.chung.tu.ghi.so.chi.tiet'
        res = {}
        rec_id = False
        for child in tag.getchildren():
            if child.tag == 'RefDetailID':
                rec_id = child.text
            elif child.tag == 'RefID':
                rid = self.env.ref('{}.{}'.format(MODULE, child.text), False)
                if rid:
                    res['CHUNG_TU_GHI_SO_ID'] = rid.id
            elif child.tag == 'VoucherRefDate':
               res['NGAY_CHUNG_TU'] = child.text
            elif child.tag == 'VoucherPostedDate':
               res['NGAY_HACH_TOAN'] = child.text
            elif child.tag == 'VoucherRefNo':
               res['SO_CHUNG_TU'] = child.text
            elif child.tag == 'Description':
               res['DIEN_GIAI'] = child.text
            elif child.tag == 'DebitAccount':
                rid =self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if rid:
                    res['TK_NO_ID'] = rid.id 
            elif child.tag == 'CreditAccount':
                rid =self.env['danh.muc.he.thong.tai.khoan'].search([('SO_TAI_KHOAN', '=', child.text)], limit=1)
                if rid:
                    res['TK_CO_ID'] = rid.id 
            elif child.tag == 'Amount':
               res['SO_TIEN'] = float(child.text)
            elif child.tag == 'SortOrder':
                res['STT'] = int(child.text)
            elif child.tag == 'VoucherRefType':
                rid = self.env['danh.muc.reftype'].search( [('REFTYPE', '=', child.text)], limit=1)
                if rid:
                    res['LOAI_CHUNG_TU'] = rid.REFTYPENAME
            elif child.tag == 'CurrencyID':
                rid= self.env['res.currency'].search([('MA_LOAI_TIEN', '=', child.text)], limit=1)
                if rid:
                    res['currency_id'] = rid.id
        return self.env['ir.model.data']._update(rec_model, MODULE, res, rec_id, noupdate=0, mode='update', return_id=False)
    


 