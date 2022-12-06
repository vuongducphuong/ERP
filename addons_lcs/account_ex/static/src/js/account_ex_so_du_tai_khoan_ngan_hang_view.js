odoo.define('account_ex.account_ex_so_du_tai_khoan_ngan_hang_list_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');

    var AccountExSoDuTaiKhoanController = FormController.extend({

        onViewLoaded: function(e, defer) {
            var self = this;
			var def = defer;
            //this.params.ct_theo_dt
            var pr = self.params.tham_so;
            self.changeFieldValue('currency_id', pr.loai_tien_so_du_tai_khoan_ngan_hang_id.id);
            // self.changeFieldValue('SO_TAI_KHOAN_ID', pr.tai_khoan_id);
            if(pr.loai_tien_so_du_tai_khoan_ngan_hang_id.display_name == "VND"){
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
                    'loai_tien_id' : pr.loai_tien_so_du_tai_khoan_ngan_hang_id.id,
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
        onFieldChanged: function(field){
            var self =this;
            if("currency_id" == field){
                var loai_tien_id = this.getFieldValue(field).id;
                var pr = self.params.tham_so;       
                this.rpc_action({
                    model: 'account.ex.so.du.tai.khoan',
                    method: 'lay_so_du_tai_khoan',
                    args: {
                        'ct_theo_dt' : pr.ct_theo_dt,
                        'ct_theo_tk' : pr.ct_theo_tk,
                        'loai_doi_tuong' : pr.loai_doi_tuong,
                        'loai_tien_id' : loai_tien_id,
                    },
                    callback: function(result) {
                        if (result) {
                            self.updateUI(result);
                        }					
                    }
                });
            }
            
        }
    });
    
    var PurchaseDocumentView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: AccountExSoDuTaiKhoanController,
        }),
    });
    
    view_registry.add('account_ex_so_du_tai_khoan_ngan_hang_list_view', PurchaseDocumentView);
    
    return PurchaseDocumentView;
});