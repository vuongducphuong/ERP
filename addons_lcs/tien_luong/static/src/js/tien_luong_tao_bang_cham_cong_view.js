odoo.define('tien_luong.tien_luong_tao_bang_cham_cong_form_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
   
    var TienLuongTaoBangChamCongController = FormController.extend({
        onViewLoaded: function(e, defer) {
            var def = defer;
            this.getFieldWidget('BANG_CHAM_CONG').changeDomain([['ten_loai_cham_cong','=','Bảng chấm công theo buổi']]);
            if (def) {
                def.resolve();
            }
        },

        onFieldChanged: function(field){
            var self = this;
            if (field == 'LOAI_CHAM_CONG'){
                var LOAI_CHAM_CONG = this.getFieldValue('LOAI_CHAM_CONG')
                if (LOAI_CHAM_CONG == 'CHAM_CONG_THEO_BUOI'){
                    self.getFieldWidget('BANG_CHAM_CONG').changeDomain([['ten_loai_cham_cong','=','Bảng chấm công theo buổi']]);
                }
                else{
                    self.getFieldWidget('BANG_CHAM_CONG').changeDomain([['ten_loai_cham_cong','=','Bảng chấm công theo giờ']]);
                }
            }
            
        }
    });
    
    var TienLuongTaoBangChamCongView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: TienLuongTaoBangChamCongController,
        }),
    });
    
    view_registry.add('tien_luong_tao_bang_cham_cong_form_view', TienLuongTaoBangChamCongView);
    
    return TienLuongTaoBangChamCongView;
});
