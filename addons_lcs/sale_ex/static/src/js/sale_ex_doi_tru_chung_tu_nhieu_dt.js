odoo.define('sale_ex.doi_tru_nhieu_doi_tuong_form_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormRenderer = require('web.FormRenderer');
    var BasicModel = require('web.BasicModel');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');

    var DoiTruNhieuDoiTuongFormController = FormController.extend({
        init: function () {
            this._super.apply(this, arguments);
        },
        // custom_events: _.extend({}, FormController.prototype.custom_events, {
            // open_link: '_onOpenLink',
        // }),

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
                    }
                    self.changeFieldValue('LAY_DU_LIEU_JSON', tham_so);
                    break;

                case "btn_thuc_hien":
                    self.changeFieldValue('STEP', 2);
                    this.rpc_action({
                        model: 'sale.ex.doi.tru.chung.tu.nhieu.doi.tuong',
                        method: 'thuc_hien_doi_tru',
                        // args: {},
                        callback: function(result) {
                            self.updateUI(result);
                            $('button[name="btn_thuc_hien"]').text('Hoàn thành');
                        }
                    })
                    break;
                case "btn_quay_lai":
                    self.changeFieldValue('STEP', 1);
                    $('button[name="btn_thuc_hien"]').text('Thực hiện');
                    break;
                default: 
                   this._super.apply(this, arguments);
            }
            
        },

        _onOpenLink: function (event) {
            event.stopPropagation();
            var self = this;    
            var colName = event.data.colName;
            var record = this.model.get(event.data.recordId);
            return new dialogs.FormViewDialog(self, {
                //fields_view: data.fields_view,
                model: this.model,
                //parentID: data.parentID,
                readonly: false,
                recordID: record.id,
                res_id: record.res_id,
                res_model: record.model,
                shouldSaveLocally: true,
                disable_multiple_selection: true,
                title: "Chi tiết đối trừ chứng từ",
                field: event.data.field,
            }).open();
        },
    });

    var DoiTruNhieuDoiTuongTuXKBHRenderer = FormRenderer.extend({
        init: function () {
            this._super.apply(this, arguments);
        },
    });

    var DoiTruNhieuDoiTuongFormModel = BasicModel.extend({
        init: function () {
            this._super.apply(this, arguments);
        },
    });
    
    var DoiTruNhieuDoiTuongFormView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Model: DoiTruNhieuDoiTuongFormModel,
            Renderer: DoiTruNhieuDoiTuongTuXKBHRenderer,
            Controller: DoiTruNhieuDoiTuongFormController,
        }),
    });
    
    view_registry.add('doi_tru_nhieu_doi_tuong_form_view', DoiTruNhieuDoiTuongFormView);
    
    return DoiTruNhieuDoiTuongFormView;
});
