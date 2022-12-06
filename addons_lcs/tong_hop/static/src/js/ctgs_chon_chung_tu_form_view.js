odoo.define('tong_hop.ctgs_chon_chung_tu_form_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormRenderer = require('web.FormRenderer');
    var BasicModel = require('web.BasicModel');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');

    var CtgsChonChungTuFormController = FormController.extend({
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
                    var params;
                    var loai_chung_tu_id;
                    if(self.params.tham_so){
                        params = self.params.tham_so;
                    }
                    if(current_data.LOAI_CHUNG_TU_ID == false){
                        loai_chung_tu_id = -1
                    }
                    else{
                        loai_chung_tu_id = current_data.LOAI_CHUNG_TU_ID.data.id
                    }
                    this.rpc_action({
                        model: 'tong.hop.ctgs.chon.chung.tu.form',
                        method: 'lay_du_lieu_chung_tu',
                        args: {
                            'tu_ngay' : current_data.TU_NGAY,
                            'den_ngay' : current_data.DEN_NGAY,
                            'loai_chung_tu_id' : loai_chung_tu_id,
                            'params' : params,
                        },
                        callback: function(result) {
                            if (result) {
                                self.updateUI(result);
                            }					
                        }
                    });
                    break;

                default: 
                   this._super.apply(this, arguments);
            }
            
        }
    });

    var CtgsChonChungTuTuXKBHRenderer = FormRenderer.extend({
        init: function () {
            this._super.apply(this, arguments);
        },
    });

    var CtgsChonChungTuFormModel = BasicModel.extend({
        init: function () {
            this._super.apply(this, arguments);
        },
    });
    
    var CtgsChonChungTuFormView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Model: CtgsChonChungTuFormModel,
            Renderer: CtgsChonChungTuTuXKBHRenderer,
            Controller: CtgsChonChungTuFormController,
        }),
    });
    
    view_registry.add('ctgs_chon_chung_tu_form_view', CtgsChonChungTuFormView);
    
    return CtgsChonChungTuFormView;
});
