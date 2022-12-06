odoo.define('stock_ex.nhap_kho_form_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');

    var NhapKhoFormController = FormController.extend({
        // init: function () {
        //     this._super.apply(this, arguments);
        // },

        getPrintBlackList:function () {
            var blackList = {};
            
            if (this.getFieldValue('type') == 'NHAP_KHO'){
                blackList['02-VT: Phiếu xuất kho'] = true;
            }
            else if (this.getFieldValue('type') == 'XUAT_KHO'){
                blackList['01-VT: Phiếu nhập kho'] = true;
            }
            else if (this.getFieldValue('type') == 'CHUYEN_KHO'){
                blackList['01-VT: Phiếu nhập kho'] = true;
                blackList['02-VT: Phiếu xuất kho'] = true;
            }
            return blackList;
        },
        _onButtonClicked: function(event) {
            var self = this;
			event.stopPropagation();
            switch (event.data.attrs.name)
            {
                case "btn_nhap_ma_quy_cach":
                    var record = event.data.record.data.CHI_TIET_IDS.data[0];
                    var param = {
                        'LOAI_CHUNG_TU' : event.data.record.data.type,
                    }

                    return new dialogs.FormViewDialog(this, _.extend({}, this.nodeOptions, {
                        model: this.model,
                        readonly: false,
                        recordID: record.id,
                        res_id: record.res_id,
                        res_model: record.model,
                        shouldSaveLocally: true,
                        disable_multiple_selection: true,
                        context : param,
//                         ref_views: [['stock_ex.view_stock_ex_nhap_xuat_kho_chi_tiet_form', 'form']],
                        
                    })).open();
                    break;
                
                default: 
                   this._super.apply(this, arguments);
            }
            
        },        
    });

    
    var NhapKhoFormView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: NhapKhoFormController,
        }),
    });
    
    view_registry.add('nhap_kho_form_view', NhapKhoFormView);
    
    return NhapKhoFormView;
});

odoo.define('stock_ex.nhap_kho_list_view', function (require) {
    "use strict";

    var ListController = require('web.ListController');
    var ListView = require('web.ListView');
    var view_registry = require('web.view_registry');
   

    var NhapKhoListController = ListController.extend({
        // init: function () {
        //     this._super.apply(this, arguments);
        // },

        getPrintBlackList:function () {
            var blackList = {};
            var selectedRecords = this.getSelectedRecords();
            for (var i=0; i<selectedRecords.length; i++) {
                var record = selectedRecords[i].data;
            
                if (record.type == 'NHAP_KHO'){
                    blackList['02-VT: Phiếu xuất kho'] = true;
                }
                else if (record.type == 'XUAT_KHO'){
                    blackList['01-VT: Phiếu nhập kho'] = true;
                }
                else if (record.type == 'CHUYEN_KHO'){
                    blackList['01-VT: Phiếu nhập kho'] = true;
                    blackList['02-VT: Phiếu xuất kho'] = true;
                }
            }
            return blackList;
        },
        
    });

    
    var NhapKhoListView = ListView.extend({
        config: _.extend({}, ListView.prototype.config, {
            Controller: NhapKhoListController,
        }),
    });
    
    view_registry.add('nhap_kho_list_view', NhapKhoListView);
    
    return NhapKhoListView;
});
