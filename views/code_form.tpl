<div class="bs-docs-section">
  <div class="row">
    <div class="col-lg-6 col-lg-offset-3">
      <div class="well bs-component">
        <form class="form-horizontal" action="/view" method="post">
          <fieldset>
            <legend>Edit Abstract</legend>
            %if var:
              <div class="alert alert-dismissible alert-danger">
                <button type="button" class="close" data-dismiss="alert">×</button>
                {{ var }}
              </div>
            %end
            <div class="form-group">
              <label for="reference_code" class="col-lg-2 control-label">Code</label>
              <div class="col-lg-10">
                <input class="form-control" name="reference_code" placeholder="Your reference code" type="text"></input>
              </div>
            </div>
            <div class="form-group">
              <div class="col-lg-10 col-lg-offset-2">
                <button type="submit" class="btn btn-primary">View</button>
              </div>
            </div>
          </fieldset>
        </form>
      <div style="display: none;" name="source-button" class="btn btn-primary btn-xs">&lt; &gt;</div></div>
    </div>    
  </div>
</div>
