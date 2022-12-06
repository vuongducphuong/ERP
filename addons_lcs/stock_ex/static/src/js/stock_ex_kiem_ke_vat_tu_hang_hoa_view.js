odoo.define('stock_ex.stock_ex_kiem_ke_bang_kiem_ke_vat_tu_hang_hoa_form_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');

    var KiemKeVatTuHangHoaController = FormController.extend({
        custom_events: _.extend({}, FormController.prototype.custom_events, {
            'xem_ma_quy_cach': '_onXemMaQuyCach',
        }),

        _onCreate: function() {
            var self = this;
            new dialogs.FormViewDialog(this, {
                readonly: false,
                res_model: 'stock.ex.kiem.ke.vat.tu.hang.hoa',
                title: 'Kiểm kê vật tư, hàng hóa',
                ref_views: [['stock_ex.view_stock_ex_kiem_ke_vat_tu_hang_hoa_tham_so_form', 'form']],
                size : 'large',
                disable_multiple_selection: true,
                shouldSaveLocally: true,
                on_before_saved: function(controller) {
                    var def = $.Deferred();
					var error = [];
                    var ngay_hach_toan = controller.getFieldValue('NGAY_BAT_DAU_HACH_TOAN');
                    var den_ngay = controller.getFieldValue('DEN_NGAY');
                    if(den_ngay < ngay_hach_toan ){
                        error = 'Ngày không được nhỏ hơn ngày bắt đầu dữ liệu kế toán. Xin vui lòng kiểm tra lại.';
                        self.notifyInvalidFields(error);
                        def.resolve(false);
                    }
                    def.resolve(true);
                    return def;   
                },
                on_after_saved: function (record, changed) {
                    if (changed) {
                        var context = {
                            'default_KIEM_KE_KHO_ID':record.data.KIEM_KE_KHO_ID.data.id,
                            'default_DEN_NGAY': record.data.DEN_NGAY,
                            'default_CHI_TIET_THEO': record.data.CHI_TIET_THEO_SELECTION,
                            'default_DON_VI_TINH': record.data.DON_VI_TINH,
                            'default_LAY_TAT_CA_VAT_TU': record.data.LAY_TAT_CA_VAT_TU,
                        }
                    
                         self.createRecord(context);
                    }

                },
            }).open();
            
        },

        _onButtonClicked: function(event) {
            var self = this;
			event.stopPropagation();
            switch (event.data.attrs.name)
            {
                case "btn_nhap_ma_quy_cach":
                    var record = event.data.record.data.STOCK_EX_BANG_KIEM_KE_VTHH_CAN_DIEU_CHINH_CHI_TIET_FORM_IDS.data[0];
                    // var param = {
                    //     'LOAI_CHUNG_TU' : event.data.record.data.type,
                    // }

                    return new dialogs.FormViewDialog(this, _.extend({}, this.nodeOptions, {
                        model: this.model,
                        readonly: false,
                        recordID: record.id,
                        res_id: record.res_id,
                        res_model: record.model,
                        shouldSaveLocally: true,
                        disable_multiple_selection: true,
                        // context : param,
                        ref_views: [['stock_ex.view_stock_ex_nhap_xuat_kho_chi_tiet_form', 'form']],
                        
                    })).open();
                    break;
                
                default: 
                   this._super.apply(this, arguments);
            }
            
        },

        onRowChanged: function(field, columnName, newValue, recordValue, record) {
            var localData = this.getLocalData();
            if (columnName == 'MA_HANG_ID' && recordValue['CO_MA_QUY_CACH']) {
                return new dialogs.FormViewDialog(this, {
                        model: this.model,
                        readonly: false,
                        recordID: record && record.id,
                        res_id: record && record.res_id,
                        res_model: 'stock.ex.bang.kiem.ke.vthh.can.dieu.chinh.chi.tiet.form',
                        shouldSaveLocally: true,
                        disable_multiple_selection: true,
                        localData: localData,
                    }).open();
            }
            return true;
        },

        _onXemMaQuyCach: function(ev) {
            ev.stopPropagation();
            return new dialogs.FormViewDialog(this, {
                model: this.model,
                readonly: false,
                recordID: ev.data.row.key,
                res_model: 'stock.ex.bang.kiem.ke.vthh.can.dieu.chinh.chi.tiet.form',
                shouldSaveLocally: true,
                disable_multiple_selection: true,
                //ref_views: [['stock_ex.view_stock_ex_nhap_xuat_kho_chi_tiet_form', 'form']],

            }).open();
        }
    });
    
    var KiemKeVatTuHangHoaView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: KiemKeVatTuHangHoaController,
        }),
    });
    
    view_registry.add('stock_ex_kiem_ke_bang_kiem_ke_vat_tu_hang_hoa_form_view', KiemKeVatTuHangHoaView);
    
    return KiemKeVatTuHangHoaView;
});

odoo.define('stock_ex.stock_ex_kiem_ke_bang_kiem_ke_vat_tu_hang_hoa_list_view', function (require) {
    "use strict";

    var ListController = require('web.ListController');
    var ListView = require('web.ListView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');

    var KiemKeVatTuHangHoaController = ListController.extend({
        _onCreate: function() {
            var self = this;
            new dialogs.FormViewDialog(this, {
                readonly: false,
                res_model: 'stock.ex.kiem.ke.vat.tu.hang.hoa',
                title: 'Kiểm kê vật tư, hàng hóa',
                ref_views: [['stock_ex.view_stock_ex_kiem_ke_vat_tu_hang_hoa_tham_so_form', 'form']],
                size : 'large',
                disable_multiple_selection: true,
                shouldSaveLocally: true,
                on_before_saved: function(controller) {
                    var def = $.Deferred();
					var error = [];
                    var ngay_hach_toan = controller.getFieldValue('NGAY_BAT_DAU_HACH_TOAN');
                    var den_ngay = controller.getFieldValue('DEN_NGAY');
                    if(den_ngay < ngay_hach_toan ){
                        error = 'Ngày không được nhỏ hơn ngày bắt đầu dữ liệu kế toán. Xin vui lòng kiểm tra lại.';
                        self.notifyInvalidFields(error);
                        def.resolve(false);
                    }
                    def.resolve(true);
                    return def;   
                },
                on_after_saved: function (record, changed) {
                    if (changed) {
                        var context = {
                            'default_KIEM_KE_KHO_ID':record.data.KIEM_KE_KHO_ID.data.id,
                            'default_DEN_NGAY': record.data.DEN_NGAY,
                            'default_CHI_TIET_THEO': record.data.CHI_TIET_THEO_SELECTION,
                            'default_DON_VI_TINH': record.data.DON_VI_TINH,
                            'default_LAY_TAT_CA_VAT_TU': record.data.LAY_TAT_CA_VAT_TU,
                        }
                    
                         self.createRecord(context);
                    }

                },
            }).open();
            
        },
    });
    
    var KiemKeVatTuHangHoaView = ListView.extend({
        config: _.extend({}, ListView.prototype.config, {
            Controller: KiemKeVatTuHangHoaController,
        }),
    });
    
    view_registry.add('stock_ex_kiem_ke_bang_kiem_ke_vat_tu_hang_hoa_list_view', KiemKeVatTuHangHoaView);
    
    return KiemKeVatTuHangHoaView;

});
