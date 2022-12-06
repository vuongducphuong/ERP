odoo.define('supply.chon_chung_tu_ghi_giam_form_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormRenderer = require('web.FormRenderer');
    var BasicModel = require('web.BasicModel');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');

    var ChonChungTuGhiGiamFormController = FormController.extend({
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
                        'TU_NGAY' : current_data.TU_NGAY,
                        'DEN_NGAY' : current_data.DEN_NGAY,
                    }
                    self.changeFieldValue('LAY_DU_LIEU_JSON', tham_so);
                    break;

                default: 
                   this._super.apply(this, arguments);
            }
            
        }
    });

    var ChonChungTuGhiGiamXKBHRenderer = FormRenderer.extend({
        init: function () {
            this._super.apply(this, arguments);
        },
    });

    var ChonChungGhiGiamFormModel = BasicModel.extend({
        init: function () {
            this._super.apply(this, arguments);
        },
    });
    
    var ChonChungGhiGiamFormView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Model: ChonChungGhiGiamFormModel,
            Renderer: ChonChungTuGhiGiamXKBHRenderer,
            Controller: ChonChungTuGhiGiamFormController,
        }),
    });
    
    view_registry.add('chon_chung_tu_ghi_giam_form_view', ChonChungGhiGiamFormView);
    
    return ChonChungGhiGiamFormView;
});
