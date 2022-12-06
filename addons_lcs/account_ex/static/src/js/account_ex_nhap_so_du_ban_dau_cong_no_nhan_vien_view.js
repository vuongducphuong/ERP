odoo.define('account_ex.account_ex_nhap_so_du_ban_dau_cong_no_nhan_vien_list_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');

    var AccountExSoDuTaiKhoanController = FormController.extend({
        // custom_events: _.extend({}, FormController.prototype.custom_events, {
            // open_link: '_onOpenLink',
        // }),

        init: function (parent, model, renderer, params) {
            this._super.apply(this, arguments);
        },

        _onOpenLink: function (event) {
            event.stopPropagation();
            var self = this;    
            var colName = event.data.colName;
            var record = this.model.get(event.data.recordId);
//             Lấy số tài khoản ở master form Nhập số dư tài khoản gửi về form bật ra theo link 
            var so_tai_khoan_id = this.getFieldValue('SO_TAI_KHOAN_ID');
            var loai_tien_id = this.getFieldValue('currency_id');
            var context = {
                'TK_ID': so_tai_khoan_id,
                'currency_id': loai_tien_id,
                };
            if (colName == 'NHAP_SO_DU_CHI_TIET') {
                return new dialogs.FormViewDialog(self, {
                    model: this.model,
                    res_model: record.model,
                    params: context,
                    parent_form: self,
                    recordID: record.id,
                    res_id: record.id,
                    title: "Nhập chi tiết công nợ nhân viên",
                    ref_views: [['account_ex.view_account_ex_nhap_so_du_tai_khoan_theo_nhan_vien', 'form']],
                    readonly: false,
                    disable_multiple_selection: true,
                    shouldSaveLocally: true,
                    on_after_saved: function(record, changes) {
                        if(changes){
                            var tong_du_no_quy_doi = 0;
                            var tong_du_co_quy_doi = 0;
                            var tong_du_no_nguyen_te = 0;
                            var tong_du_co_nguyen_te = 0;
                            if(record.data.ACCOUNT_EX_SO_DU_TAI_KHOAN_CHI_TIET_THEO_DOI_TUONG_IDS.data.length > 0){
                                for(var i in record.data.ACCOUNT_EX_SO_DU_TAI_KHOAN_CHI_TIET_THEO_DOI_TUONG_IDS.data){
                                    tong_du_no_quy_doi += record.data.ACCOUNT_EX_SO_DU_TAI_KHOAN_CHI_TIET_THEO_DOI_TUONG_IDS.data[i].data.DU_NO;
                                    tong_du_co_quy_doi += record.data.ACCOUNT_EX_SO_DU_TAI_KHOAN_CHI_TIET_THEO_DOI_TUONG_IDS.data[i].data.DU_CO;
                                    tong_du_no_nguyen_te += record.data.ACCOUNT_EX_SO_DU_TAI_KHOAN_CHI_TIET_THEO_DOI_TUONG_IDS.data[i].data.DU_NO_NGUYEN_TE;
                                    tong_du_co_nguyen_te += record.data.ACCOUNT_EX_SO_DU_TAI_KHOAN_CHI_TIET_THEO_DOI_TUONG_IDS.data[i].data.DU_CO_NGUYEN_TE;
                                }
                            }
                            if(tong_du_no_quy_doi == 0 && tong_du_co_quy_doi == 0 && tong_du_no_nguyen_te == 0 && tong_du_co_nguyen_te == 0){
                                if(record.data.ACCOUNT_EX_SO_DU_TAI_KHOAN_CHI_TIET_THEO_HOA_DON_IDS.data.length > 0){
                                    for(var j in record.data.ACCOUNT_EX_SO_DU_TAI_KHOAN_CHI_TIET_THEO_HOA_DON_IDS.data){
                                        tong_du_no_quy_doi += record.data.ACCOUNT_EX_SO_DU_TAI_KHOAN_CHI_TIET_THEO_HOA_DON_IDS.data[j].data.SO_CON_PHAI_THU;
                                        tong_du_co_quy_doi += record.data.ACCOUNT_EX_SO_DU_TAI_KHOAN_CHI_TIET_THEO_HOA_DON_IDS.data[j].data.SO_THU_TRUOC;
                                        tong_du_no_nguyen_te += record.data.ACCOUNT_EX_SO_DU_TAI_KHOAN_CHI_TIET_THEO_HOA_DON_IDS.data[j].data.SO_CON_PHAI_THU_NGUYEN_TE;
                                        tong_du_co_nguyen_te += record.data.ACCOUNT_EX_SO_DU_TAI_KHOAN_CHI_TIET_THEO_HOA_DON_IDS.data[j].data.SO_THU_TRUOC_NGUYEN_TE;
                                    }
                                }
                            }
                            if(record.data.CO_HACH_TOAN_NGOAI_TE == false){
                                tong_du_no_nguyen_te = tong_du_no_quy_doi;
                                tong_du_co_nguyen_te = tong_du_co_quy_doi;
                            }
                            if(tong_du_no_quy_doi > 0 && tong_du_co_quy_doi > 0){
                                var du_no_tru_du_co = tong_du_no_quy_doi - tong_du_co_quy_doi;
                                if(du_no_tru_du_co > 0){
                                    tong_du_no_quy_doi = du_no_tru_du_co;
                                    tong_du_co_quy_doi = 0;
                                }
                                else if(du_no_tru_du_co < 0){
                                    tong_du_co_quy_doi = -1*du_no_tru_du_co;
                                    tong_du_no_quy_doi = 0;
                                }
                                else{
                                    tong_du_co_quy_doi = 0;
                                    tong_du_no_quy_doi = 0;
                                }
                            }
                            self.updateUI({'ACCOUNT_EX_SO_DU_TAI_KHOAN_CHI_TIET_IDS': [[1, record.id, {'DU_NO': tong_du_no_quy_doi,'DU_CO': tong_du_co_quy_doi,'DU_NO_NGUYEN_TE' : tong_du_no_nguyen_te,'DU_CO_NGUYEN_TE' : tong_du_co_nguyen_te}]]});
                        }
                    },
                }).open();
            }
        },

        onViewLoaded: function(e, defer) {
            var self = this;
			var def = defer;
            //this.params.ct_theo_dt
            var pr = self.params.tham_so;
            self.changeFieldValue('currency_id', pr.loai_tien_so_so_cong_no_nhan_vien_id.id);
            self.changeFieldValue('SO_TAI_KHOAN_ID', pr.tai_khoan_id);
            if(pr.loai_tien_so_so_cong_no_nhan_vien_id.display_name == "VND"){
            	self.changeFieldValue('CO_HACH_TOAN_NGOAI_TE', false);
            }
            if(pr.tai_khoan_id && (pr.ct_theo_dt == 1)){
//                 self.changeFieldValue('SO_TAI_KHOAN_ID', pr.tai_khoan_id);
            }
            if(pr.ct_theo_dt){
                self.changeFieldValue('CHI_TIET_THEO_DOI_TUONG', pr.ct_theo_dt);
            }
            if(pr.ct_theo_tk){
                self.changeFieldValue('CHI_TIET_THEO_TK_NGAN_HANG', pr.ct_theo_tk);
            }
            if(pr.loai_doi_tuong){
                self.changeFieldValue('LOAI_DOI_TUONG', pr.loai_doi_tuong);
            }
            this.rpc_action({
                model: 'account.ex.so.du.tai.khoan',
                method: 'lay_so_du_tai_khoan',
                args: {
                    'ct_theo_dt' : pr.ct_theo_dt,
                    'ct_theo_tk' : pr.ct_theo_tk,
                    'loai_doi_tuong' : pr.loai_doi_tuong,
                    'loai_tien_id' : pr.loai_tien_so_so_cong_no_nhan_vien_id.id,
                },
                callback: function(result) {
                    if (result) {
                        self.updateUI(result);
//                         self.changeFieldValue('SO_TAI_KHOAN_ID',4017);
                    }
					if (def) {
                        def.resolve();
                    }
                }
            });
        },
        getDataCongNoNhanVien:function(defer) {            
            var self = this;
            var kiemtra_gia_tri_tai_khoan =  this.getFieldValue('SO_TAI_KHOAN_ID');
            var kiem_tra_gia_tri_loai_tien = this.getFieldValue('currency_id');
            if(kiemtra_gia_tri_tai_khoan != null){
                var tai_khoan_id = this.getFieldValue('SO_TAI_KHOAN_ID').id;
            }
            else{
                var tai_khoan_id = null;
            }
            if(kiem_tra_gia_tri_loai_tien != null){
                var loai_tien_id = this.getFieldValue('currency_id').id;
            }
            else{
                var loai_tien_id = null;
            }
            var pr = self.params.tham_so;       
            this.rpc_action({
                model: 'account.ex.so.du.tai.khoan',
                method: 'lay_so_du_tai_khoan',
                args: {
                    'ct_theo_dt' : pr.ct_theo_dt,
                    'ct_theo_tk' : pr.ct_theo_tk,
                    'loai_doi_tuong' : pr.loai_doi_tuong,
                    'loai_tien_id' : loai_tien_id,
                    'tai_khoan_id' : tai_khoan_id,
                },
                callback: function(result) {
                    if (result) {
                        self.updateUI(result);
                    }
                }
            });
        },
        onFieldChanged: function(field){
            var self = this;
            if("currency_id" == field || "SO_TAI_KHOAN_ID" == field){
                self.getDataCongNoNhanVien();
            }   
        }
    });
    
    var PurchaseDocumentView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: AccountExSoDuTaiKhoanController,
        }),
    });
    
    view_registry.add('account_ex_nhap_so_du_ban_dau_cong_no_nhan_vien_list_view', PurchaseDocumentView);
    
    return PurchaseDocumentView;
});