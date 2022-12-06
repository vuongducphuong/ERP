odoo.define('tien_ich.danh_lai_so_chung_tu_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');

    var DanhLaiSoChungTuController = FormController.extend({
        init: function () {
            this._super.apply(this, arguments);
        },
       
        _onButtonClicked: function(event) {
            var self = this;
			event.stopPropagation();
            switch (event.data.attrs.id)
            {
                
                case "btn_lay_du_lieu":
                    var nhom_loai_ct_id = self.getFieldValue("NHOM_LOAI_CHUNG_TU_ID").id;
                    var tu_ngay = self.getFieldValue("TU_NGAY");
                    var den_ngay = self.getFieldValue("DEN_NGAY");
                    this.rpc_action({
                        model: 'tien.ich.danh.lai.so.chung.tu',
                        method: 'lay_du_lieu_khi_click',
                        args: {
                            'nhom_loai_ct_id' : nhom_loai_ct_id,
                            'tu_ngay' : tu_ngay,
                            'den_ngay' : den_ngay,
                        },
                        callback: function(result) {
                            self.updateUI(result);
                        }
                    })
                    break;
                case "btn_danh_lai_so_chung_tu":
                    var chi_tiet_ids = self.getFieldValue("TIEN_ICH_DANH_LAI_SO_CHUNG_TU_CHI_TIET_IDS");
//                     var so_chung_tu_moi = "PT111111";
                    var tien_to = self.getFieldValue("TIEN_TO");
                    var gia_tri_bd_so = self.getFieldValue("GIA_TRI_BAT_DAU_PHAN_SO");
                    var tong_so_ky_tu = self.getFieldValue("TONG_SO_KY_TU_PHAN_SO");
                    var hau_to = self.getFieldValue("HAU_TO");
                    var so_chung_tu_moi = '';
                    var chi_tiet_ids_moi = [[5]];
                    for(var i in chi_tiet_ids){
//                         so_chung_tu_moi = tien_to + this.zeroPad(gia_tri_bd_so,tong_so_ky_tu) + hau_to;
//                         gia_tri_bd_so += 1;
                        var newval = chi_tiet_ids[i];
                        _.extend(newval,{'SO_CHUNG_TU_MOI': "so_chung_tu_moi"});
                        chi_tiet_ids_moi.push([0, 0, newval]);
                    }
                    this.updateUI({'TIEN_ICH_DANH_LAI_SO_CHUNG_TU_CHI_TIET_IDS': chi_tiet_ids_moi});
//                     this.rpc_action({
//                         model: 'tien.ich.danh.lai.so.chung.tu',
//                         method: 'btn_cat',
//                         args: {
//                             'chi_tiet_ids' : chi_tiet_ids,
//                             'so_chung_tu_moi' : so_chung_tu_moi,
//                         },
//                         callback: function(result) {
//                             self.updateUI(result);
//                         }
                       
//                     })
                    break;

                case "btn_cat":
                    var chi_tiet_ids = self.getFieldValue("TIEN_ICH_DANH_LAI_SO_CHUNG_TU_CHI_TIET_IDS");
                    var so_chung_tu_moi = "PT111111"
                    this.rpc_action({
                        model: 'tien.ich.danh.lai.so.chung.tu',
                        method: 'btn_cat',
                        args: {
                            'chi_tiet_ids' : chi_tiet_ids,
                            'so_chung_tu_moi' : so_chung_tu_moi,
                        },
                        callback: function(result) {
                            self.updateUI(result);
                        }
                    })
                    break;

                default: 
                   this._super.apply(this, arguments);
            }
            
        },
        zeroPad: function(num, places) {
         var zero = places - num.toString().length + 1;
         return Array(+(zero > 0 && zero)).join("0") + num;
        }
       
    });



    
    var DanhLaiSoChungTuView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: DanhLaiSoChungTuController,
        }),
    });
    
    view_registry.add('danh_lai_so_chung_tu_view', DanhLaiSoChungTuView);
    
    return DanhLaiSoChungTuView;
});
