odoo.define('account_ex.account_ex_ton_kho_vthh_form_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');

    var Dialog = require('web.Dialog');

    var TonKhoVTHHController = FormController.extend({
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
            var def = $.Deferred();
            var error = [];
            var record = this.model.get(event.data.recordId);
        // var context = {};
            if(record.data.THEO_DOI_THEO_MA_QUY_CACH == true){
                 return new dialogs.FormViewDialog(self, {
                    model: this.model,
                    res_model:'stock.ex.bang.kiem.ke.vthh.can.dieu.chinh.chi.tiet.form',
                    readonly: false,
                    parent_form: self,
                    recordID: record.id,
                    res_id: record.res_id,
                    title: "Nhập mã quy cách",
                    ref_views: [['stock_ex.view_stock_ex_kiem_ke_kho_chi_tiet_form', 'form']],
                    readonly: false,
                    disable_multiple_selection: true,
                    field: event.data.field,
                }).open();
            }
            else{
                    error = 'Bạn phải chọn vật tư có tích chọn theo dõi theo mã quy cách để nhập mã quy cách.';
                }
            if (error.length) {
                self.notifyInvalidFields(error);
                def.resolve(false);
            } else {
                def.resolve(true);
            }
            return def;  
            },
           

        onViewLoaded: function(e, defer) {
            var self = this;
			var def = defer;
			var pr = self.params.tham_so;
			if(pr.kho_id){
			    self.changeFieldValue('KHO_ID', pr.kho_id);
			}
            this.rpc_action({
                model: 'account.ex.ton.kho.vat.tu.hang.hoa.master',
                method: 'ton_kho_vat_tu_hang_hoa',
                args: {
                    'kho_id' : pr.kho_id,
                },
                callback: function(result) {
                    if (result) {
                        self.updateUI(result);
                    }
					if (def) {
                        def.resolve();
                    }
                }
            });
        },
        onFieldChanged: function(field){
            var self = this;
            if("KHO_ID"==field){
            	var kho_id = false;
            	if(this.getFieldValue('KHO_ID')){
            		kho_id = this.getFieldValue('KHO_ID').id;
            	}
                this.rpc_action({
                model: 'account.ex.ton.kho.vat.tu.hang.hoa.master',
                method: 'ton_kho_vat_tu_hang_hoa',
                args: {
                    'kho_id': kho_id,
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
    
    var TonKhoVTHHView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: TonKhoVTHHController,
        }),
    });
    
    view_registry.add('account_ex_ton_kho_vthh_form_view', TonKhoVTHHView);
    
    return TonKhoVTHHView;
});