odoo.define('supply.dieu_chinh_cong_cu_dung_cu_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormRenderer = require('web.FormRenderer');
    var BasicModel = require('web.BasicModel');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');

    var DieuChinhCongCuDungCuController = FormController.extend({
        init: function () {
            this._super.apply(this, arguments);
        },

        _onButtonClicked: function(event) {
            var self = this;
			event.stopPropagation();
            switch (event.data.attrs.id)
            {
                
                case "btn_chon_chung_tu":
                    var context = {};
                    var default_chi_tiet = [];
                    var current_data = event.data.record.data;
                    var chi_tiet_ids = current_data.SUPPLY_TAP_HOP_CHUNG_TU_CCDC_IDS.data;
                    for (var i = 0; i<chi_tiet_ids.length; i++){
                        var chi_tiet = chi_tiet_ids[i].data;
                        default_chi_tiet.push((0, 0, {
                            'ID_GOC' : chi_tiet.ID_GOC,
                            'MODEL_GOC' : chi_tiet.MODEL_GOC,
                            'CHUNG_TU_CHON' : 'DIEU_CHINH',
                        }))
                    }
                    context['default_CHUNG_TU_CHON'] = 'DIEU_CHINH';
                    context['ACCOUNT_EX_CHON_CHUNG_TU_CHI_TIET_IDS'] = default_chi_tiet;
                    // return new dialogs.SelectParamsDialog(this, _.extend({}, this.nodeOptions, {
                    //     res_model: 'account.ex.chon.chung.tu.form',
                    //     title: 'Chọn chứng từ',
                    //     ref_views: [['account_ex.view_account_ex_chon_chung_tu_form_form', 'form']],
                    //     context: context,
                    //     on_selected: function (records) {
                    //         self.changeFieldValue('CHON_CHUNG_TU_JSON', records)
                    //     },
                    // })).open();


                    return new dialogs.FormViewDialog(this,{
                        res_model: 'account.ex.chon.chung.tu.form',
                        title: 'Chọn chứng từ',
                        ref_views: [['account_ex.view_account_ex_chon_chung_tu_form_form', 'form']],
                        context: context,
                        shouldSaveLocally: true,
                        on_after_saved: function (record, changed) {
                            if (changed) {
                                if(record.data.ACCOUNT_EX_CHON_CHUNG_TU_CHI_TIET_IDS.data.length > 0){
                                    var arr_chung_tu_chi_tiet = [[5]];
                                    for(var i in record.data.ACCOUNT_EX_CHON_CHUNG_TU_CHI_TIET_IDS.data){
                                        var chi_tiet = record.data.ACCOUNT_EX_CHON_CHUNG_TU_CHI_TIET_IDS.data[i].data;
                                        if(chi_tiet.AUTO_SELECT == true){
                                            arr_chung_tu_chi_tiet.push([0, 0, {
                                                
                                                'NGAY_CHUNG_TU': chi_tiet.NGAY_CHUNG_TU,
                                                'SO_CHUNG_TU': chi_tiet.SO_CHUNG_TU,
                                                'DIEN_GIAI': chi_tiet.DIEN_GIAI,
                                                
                                                'SO_TIEN': chi_tiet.SO_TIEN,
                                                'ID_GOC': chi_tiet.ID_GOC,                                               
                                                'MODEL_GOC': chi_tiet.MODEL_GOC,
                                            }])
                                        }
                                        
                                    }
                                }
                                self.updateUI({'SUPPLY_TAP_HOP_CHUNG_TU_CCDC_IDS': arr_chung_tu_chi_tiet});
                            }
                        },
                    }).open();
					break;

                default: 
                   this._super.apply(this, arguments);
            }
            
        }
    });

    var DieuChinhCongCuDungCuRenderer = FormRenderer.extend({
        init: function () {
            this._super.apply(this, arguments);
        },
    });

    var DieuChinhCongCuDungCuModel = BasicModel.extend({
        init: function () {
            this._super.apply(this, arguments);
        },
    });
    
    var DieuChinhCongCuDungCuView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Model: DieuChinhCongCuDungCuModel,
            Renderer: DieuChinhCongCuDungCuRenderer,
            Controller: DieuChinhCongCuDungCuController,
        }),
    });
    
    view_registry.add('dieu_chinh_cong_cu_dung_cu_view', DieuChinhCongCuDungCuView);
    
    return DieuChinhCongCuDungCuView;
});
