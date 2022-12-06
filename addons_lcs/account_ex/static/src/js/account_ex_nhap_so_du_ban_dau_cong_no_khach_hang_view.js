odoo.define('account_ex.account_ex_nhap_so_du_ban_dau_cong_no_khach_hang_list_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');
    var Dialog = require('web.Dialog');

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
                    title: "Nhập chi tiết công nợ khách hàng",
                    ref_views: [['account_ex.view_account_ex_nhap_chi_tiet_cong_no_khach_hang_form', 'form']],
//                     size:'large',
                    readonly: false,
                    disable_multiple_selection: true,
                    shouldSaveLocally: true,
                    on_before_saved: function(controller) {
                        var def = $.Deferred();
              
                        var isDef = false;
						var error = [];
                        var so_du_tai_khoan_chi_tiet_theo_hd = controller.getFieldValue('ACCOUNT_EX_SO_DU_TAI_KHOAN_CHI_TIET_THEO_HOA_DON_IDS');
                        if(so_du_tai_khoan_chi_tiet_theo_hd.length > 0){
                            var gia_tri_hoa_don = 0;
                            var gia_tri_hoa_don_quy_doi = 0;
                            var so_con_phai_thu = 0;
                            var so_con_phai_thu_quy_doi = 0;
                            var so_thu_truoc = 0;
                            var so_thu_truoc_quy_doi = 0;
                            for(var j in so_du_tai_khoan_chi_tiet_theo_hd){
                                var check_chi_tiet_theo_hoa_don = so_du_tai_khoan_chi_tiet_theo_hd[j]
                                gia_tri_hoa_don = check_chi_tiet_theo_hoa_don.GIA_TRI_HOA_DON_NGUYEN_TE;
                                gia_tri_hoa_don_quy_doi += check_chi_tiet_theo_hoa_don.GIA_TRI_HOA_DON;
                                so_con_phai_thu += check_chi_tiet_theo_hoa_don.SO_CON_PHAI_THU_NGUYEN_TE;
                                so_con_phai_thu_quy_doi += check_chi_tiet_theo_hoa_don.SO_CON_PHAI_THU;
                                so_thu_truoc += check_chi_tiet_theo_hoa_don.SO_THU_TRUOC_NGUYEN_TE;
                                so_thu_truoc_quy_doi += check_chi_tiet_theo_hoa_don.SO_THU_TRUOC;
                            }
                            if((so_thu_truoc > 0 || so_thu_truoc_quy_doi > 0) && ((gia_tri_hoa_don > 0 || gia_tri_hoa_don_quy_doi > 0) || (so_con_phai_thu > 0 || so_con_phai_thu_quy_doi > 0))){
                                error = 'Một dòng không được nhập đồng thời cả giá trị hóa đơn/ Số còn phải thu và số thu trước. Bạn vui lòng kiểm tra lại.';
                            }
                        }
                        if (error.length) {
							self.notifyInvalidFields(error);
							def.resolve(false);
						} else {
							def.resolve(true);
						}
						return def;                           
                    },
                    on_after_saved: function(record, changes) {
                        if(changes){
                            var tong_du_no_quy_doi = 0;
                            var tong_du_co_quy_doi = 0;
                            var tong_du_no_nguyen_te = 0;
                            var tong_du_co_nguyen_te = 0;
                            if(record.data.ACCOUNT_EX_SO_DU_TAI_KHOAN_CHI_TIET_THEO_DOI_TUONG_IDS.data.length > 0){
                                for(var i in record.data.ACCOUNT_EX_SO_DU_TAI_KHOAN_CHI_TIET_THEO_DOI_TUONG_IDS.data){
                                    var chi_tiet_theo_doi_tuong = record.data.ACCOUNT_EX_SO_DU_TAI_KHOAN_CHI_TIET_THEO_DOI_TUONG_IDS.data[i].data
                                    tong_du_no_quy_doi += chi_tiet_theo_doi_tuong.DU_NO;
                                    tong_du_co_quy_doi += chi_tiet_theo_doi_tuong.DU_CO;
                                    tong_du_no_nguyen_te += chi_tiet_theo_doi_tuong.DU_NO_NGUYEN_TE;
                                    tong_du_co_nguyen_te += chi_tiet_theo_doi_tuong.DU_CO_NGUYEN_TE;
                                }
                            }
                            if(tong_du_no_quy_doi == 0 && tong_du_co_quy_doi == 0 && tong_du_no_nguyen_te == 0 && tong_du_co_nguyen_te == 0){
                                if(record.data.ACCOUNT_EX_SO_DU_TAI_KHOAN_CHI_TIET_THEO_HOA_DON_IDS.data.length > 0){
                                    for(var j in record.data.ACCOUNT_EX_SO_DU_TAI_KHOAN_CHI_TIET_THEO_HOA_DON_IDS.data){
                                        var chi_tiet_theo_hoa_don = record.data.ACCOUNT_EX_SO_DU_TAI_KHOAN_CHI_TIET_THEO_HOA_DON_IDS.data[j].data
                                        tong_du_no_quy_doi += chi_tiet_theo_hoa_don.SO_CON_PHAI_THU;
                                        tong_du_co_quy_doi += chi_tiet_theo_hoa_don.SO_THU_TRUOC;
                                        tong_du_no_nguyen_te += chi_tiet_theo_hoa_don.SO_CON_PHAI_THU_NGUYEN_TE;
                                        tong_du_co_nguyen_te += chi_tiet_theo_hoa_don.SO_THU_TRUOC_NGUYEN_TE;
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
            self.changeFieldValue('currency_id', pr.loai_tien_so_so_cong_no_khach_hang_id.id);
            if(pr.loai_tien_so_so_cong_no_khach_hang_id.display_name == "VND"){
            	self.changeFieldValue('CO_HACH_TOAN_NGOAI_TE', false);
            }
            self.changeFieldValue('SO_TAI_KHOAN_ID', pr.tai_khoan_id);
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
            self.changeFieldValue('SO_TAI_KHOAN_ID',pr.tai_khoan_id);
            this.rpc_action({
                model: 'account.ex.so.du.tai.khoan',
                method: 'lay_so_du_tai_khoan',
                args: {
                    'ct_theo_dt' : pr.ct_theo_dt,
                    'ct_theo_tk' : pr.ct_theo_tk,
                    'loai_doi_tuong' : pr.loai_doi_tuong,
                    'loai_tien_id' : pr.loai_tien_so_so_cong_no_khach_hang_id.id,
                    'tai_khoan_id' : pr.tai_khoan_id,
                },
                callback: function(result) {
                    if (result) {
                        self.updateUI(result).then(function(){
                            if (def) {
                                def.resolve();
                            }
                        });
                    }
                }
            });
        },
        getData:function(defer) {            
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
                self.getData();
            }
        }
   
    });
            
        
    
    var PurchaseDocumentView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: AccountExSoDuTaiKhoanController,
        }),
    });
    
    view_registry.add('account_ex_nhap_so_du_ban_dau_cong_no_khach_hang_list_view', PurchaseDocumentView);
    
    return PurchaseDocumentView;
    
});