odoo.define('account_ex.chon_chung_tu_form_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormRenderer = require('web.FormRenderer');
    var BasicModel = require('web.BasicModel');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');

    var ChonChungFormController = FormController.extend({
        init: function () {
            this._super.apply(this, arguments);
        },

        _onButtonClicked: function(event) {
            event.stopPropagation();
            var self = this;
            switch (event.data.attrs.name)
            {
                
                // case "btn_lay_du_lieu":
                //     var tham_so = {};
                //     var default_chi_tiet = [];
                //     // Lấy data hiện tại của form
                //     var current_data = event.data.record.data;
                //     // Lấy data của chứng từ chi tiết
                //     tham_so = {
                //         'LOAI' : current_data.LOAI_CHUNG_TU,
                //         'TU_NGAY' : current_data.TU_NGAY,
                //         'DEN_NGAY' : current_data.DEN_NGAY,
                //     }
                //     self.changeFieldValue('LAY_DU_LIEU_JSON', tham_so);
                //     break;
                case "btn_lay_du_lieu":
                    var loai_chung_tu = this.getFieldValue('LOAI_CHUNG_TU');
                    var tu_ngay = this.getFieldValue('TU_NGAY');
                    var den_ngay = this.getFieldValue('DEN_NGAY');
                    this.rpc_action({
                        model: 'account.ex.chon.chung.tu.form',
                        method: 'lay_du_lieu_cac_chung_tu',
                        args: {
                            'loai_chung_tu' : loai_chung_tu,
                            'tu_ngay' : tu_ngay,
                            'den_ngay' : den_ngay,
                        },
                        callback: function(result) {
                            if (result) {
                                self.updateUI({'ACCOUNT_EX_CHON_CHUNG_TU_CHI_TIET_IDS':result});
                            }
                        }
                    });
                    break;
                

                default: 
                   this._super.apply(this, arguments);
            }
            
        }
    });

    var ChonChungTuXKBHRenderer = FormRenderer.extend({
        init: function () {
            this._super.apply(this, arguments);
        },
    });

    var ChonChungFormModel = BasicModel.extend({
        init: function () {
            this._super.apply(this, arguments);
        },
    });
    
    var ChonChungFormView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Model: ChonChungFormModel,
            Renderer: ChonChungTuXKBHRenderer,
            Controller: ChonChungFormController,
        }),
    });
    
    view_registry.add('chon_chung_tu_form_view', ChonChungFormView);
    
    return ChonChungFormView;
});
