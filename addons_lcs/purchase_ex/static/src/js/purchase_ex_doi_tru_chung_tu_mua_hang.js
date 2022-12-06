odoo.define('purchase_ex.chon_chung_tu_mua_hang_form_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormRenderer = require('web.FormRenderer');
    var BasicModel = require('web.BasicModel');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');

    var DoiTruChungTuMuaHangFormController = FormController.extend({
        init: function () {
            this._super.apply(this, arguments);
        },

        _onButtonClicked: function(event) {
            var self = this;
			event.stopPropagation();
            switch (event.data.attrs.name)
            {
                
                case "btn_lay_du_lieu":
                    var tham_so = {};
                    var default_chi_tiet = [];
                    // Lấy data hiện tại của form
                    var current_data = event.data.record.data;
                    // Lấy data của chứng từ chi tiết
                    tham_so = {
                        'NGAY' : current_data.NGAY_DOI_TRU,
                        'currency_id' : current_data.currency_id.data.id,
                        'DOI_TUONG_ID' : current_data.DOI_TUONG_ID.data.id,
                    }
                    self.changeFieldValue('LAY_DU_LIEU_JSON', tham_so);
                    break;

                default: 
                   this._super.apply(this, arguments);
            }
            
        }

    });

    var DoiTruChungTuMuaHangTuXKBHRenderer = FormRenderer.extend({
        init: function () {
            this._super.apply(this, arguments);
        },
    });

    var DoiTruChungTuMuaHangFormModel = BasicModel.extend({
        init: function () {
            this._super.apply(this, arguments);
        },
    });
    
    var DoiTruChungTuMuaHangFormView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Model: DoiTruChungTuMuaHangFormModel,
            Renderer: DoiTruChungTuMuaHangTuXKBHRenderer,
            Controller: DoiTruChungTuMuaHangFormController,
        }),
    });
    
    view_registry.add('chon_chung_tu_mua_hang_form_view', DoiTruChungTuMuaHangFormView);
    
    return DoiTruChungTuMuaHangFormView;
});
