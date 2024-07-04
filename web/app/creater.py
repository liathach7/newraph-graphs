from matplotlib import pyplot as plt
import numpy as np

x_range=np.arange(-1.1,1.6,0.1)
y_range=[x**3 - x**2 +0.1 for x in x_range]
equation='x^3 - x^2 + 0.1'

def graph(x, y,equation):
        fig2 = plt.figure()
        ax2 = fig2.subplots()
        min_y=min(y)
        max_y=max(y)
        min_x=min(x)
        max_x=max(x)
        if min_y>0 or max_y<0:
            ax2.spines.bottom.set_bounds(min_x,max_x)
        else:
            ax2.spines['bottom'].set_position('zero')
            #ax2.xaxis.set_label_position['bottom']
        ax2.spines['top'].set_color('none')
        ax2.xaxis.tick_bottom()
        ax2.plot(x, y, c='b', label=equation)
        ax2.legend(loc='upper left')
        plt.show()
        fig2.savefig('static//eg2')

graph(x_range,y_range,equation)

<div class="modal fade" id="exampleModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
  <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="exampleModalLabel">Modal title</h5>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      <div class="modal-body">
        ...
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
        <button type="button" class="btn btn-primary">Save changes</button>
      </div>
    </div>
  </div>
</div>

<div class="bg-image" 
        style="background-image: url('../static/background.png');
                height: 100vh">
            
        </div>

const myModal = new bootstrap.Modal('#exampleModal');
            window.addEventListener('DOMContentLoaded', () => {
                myModal.show();
            });