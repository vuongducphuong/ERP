odoo.define('supply.chon_chung_tu_xk_mh', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormRenderer = require('web.FormRenderer');
    var BasicModel = require('web.BasicModel');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');

    var ChonChungTuXuatKhoMuaHangController = FormController.extend({
        init: function () {
            this._super.apply(this, arguments);
        },

        _onButtonClicked: function(event) {
            var self = this;
			event.stopPropagation();
            switch (event.data.attrs.name)
            {
                
                case "btn_chon_chung_tu":
                    var context = {};
                    var default_chi_tiet = [];
                    var current_data = event.data.record.data;
                    var chi_tiet_ids = current_data.SUPPLY_GHI_TANG_HANG_LOAT_CHI_TIET_IDS.data;
                    for (var i = 0; i<chi_tiet_ids.length; i++){
                        var chi_tiet = chi_tiet_ids[i].data;
                        default_chi_tiet.push((0, 0, {
                            'ID_GOC' : chi_tiet.ID_GOC,
                            'MODEL_GOC' : chi_tiet.MODEL_GOC,
                        }))
                    }
                    context['ACCOUNT_EX_CHON_CHUNG_TU_XUAT_KHO_MUA_HANG_CHI_TIET_IDS'] = default_chi_tiet;
                    return new dialogs.SelectParamsDialog(this, _.extend({}, this.nodeOptions, {
                        res_model: 'account.ex.chon.chung.tu.xuat.kho.mua.hang',
                        title: 'Chọn chứng từ xuất kho/ mua hàng',
                        ref_views: [['account_ex.view_account_ex_chon_chung_tu_xuat_kho_mua_hang_tham_so_form', 'form']],
                        context: context,
                        on_selected: function (records) {
                            self.changeFieldValue('CHUNG_TU_JSON', records)
                        },
                    })).open();
					break;

                case "btn_chon_chung_tu_ghi_giam":
                    var context = {};
                    var default_chi_tiet = [];
                    var current_data = event.data.record.data;
                    var chi_tiet_ids = current_data.SUPPLY_GHI_TANG_HANG_LOAT_CHI_TIET_IDS.data;
                    for (var i = 0; i<chi_tiet_ids.length; i++){
                        var chi_tiet = chi_tiet_ids[i].data;
                        default_chi_tiet.push((0, 0, {
                            'ID_GOC' : chi_tiet.ID_GOC,
                            'MODEL_GOC' : chi_tiet.MODEL_GOC,
                        }))
                    }
                    context['SUPPLY_CHON_CHUNG_TU_GHI_GIAM_TSCD_CHI_TIET_IDS'] = default_chi_tiet;
                    return new dialogs.SelectParamsDialog(this, _.extend({}, this.nodeOptions, {
                        res_model: 'supply.chon.chung.tu.ghi.giam.tscd',
                        title: 'Chọn từ chứng từ ghi giảm TSCĐ',
                        ref_views: [['supply.view_supply_chon_chung_tu_ghi_giam_tscd_tham_so_form', 'form']],
                        context: context,
                        on_selected: function (records) {
                            self.changeFieldValue('CHUNG_TU_GHI_GIAM_JSON', records)
                        },
                    })).open();
					break;

                default: 
                   this._super.apply(this, arguments);
            }
            
        }
    });

    var ChonChungTuXuatKhoMuaHangRenderer = FormRenderer.extend({
        init: function () {
            this._super.apply(this, arguments);
        },
    });

    var ChonChungTuXuatKhoMuaHangModel = BasicModel.extend({
        init: function () {
            this._super.apply(this, arguments);
        },
    });
    
    var ChonChungTuXuatKhoMuaHangView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Model: ChonChungTuXuatKhoMuaHangModel,
            Renderer: ChonChungTuXuatKhoMuaHangRenderer,
            Controller: ChonChungTuXuatKhoMuaHangController,
        }),
    });
    
    view_registry.add('chon_chung_tu_xk_mh', ChonChungTuXuatKhoMuaHangView);
    
    return ChonChungTuXuatKhoMuaHangView;
});
